from __future__ import annotations

from typing import Any, Generic, TypeVar, Unpack, cast

from pydantic import BaseModel
from sqlalchemy import asc
from sqlalchemy import delete as sql_delete
from sqlalchemy import desc
from sqlalchemy import func as sql_func
from sqlalchemy import insert
from sqlalchemy import update as sql_update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute, RelationshipProperty, strategy_options
from sqlalchemy.sql import Select, select

from src.core.types import (
    EMPTY,
    EMPTY_TYPE,
    MISSING,
    MISSING_TYPE,
    Kwargs,
    StrategyOptions,
)
from src.core.utils.filters import (
    After,
    AnyFieldFilter,
    Before,
    BeforeAfter,
    DateAdded,
    FieldFilter,
    FilterTypes,
    MonthlyFilter,
    OrderBy,
    Search,
)

from .exceptions import catch_sqlalchemy_exception
from .model import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class DAO(Generic[ModelType, CreateSchema, UpdateSchema]):
    """
    This DAO (Data Access Object) is a base class for all basic CRUD operations on the database.
    It provides a generic interface for CRUD operations on database models, with type safety through
    generics for the model and its associated schemas.

    Based first on the implementation by Sebastián Ramírez (tiangolo) in FastAPI full-stack project template:
    https://github.com/fastapi/full-stack-fastapi-template/blob/490c554e23343eec0736b06e59b2108fdd057fdc/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/app/crud/base.py
    """

    def __init__(self, model: type[ModelType]):
        self.model = model

    async def get(
        self,
        db: AsyncSession,
        _id: int,
        options: list[tuple[str, StrategyOptions]] | None = None,
        **kwargs: Unpack[Kwargs],
    ) -> ModelType | MISSING_TYPE:
        """Get single item by id."""
        statement = select(self.model).where(self.model.id == _id)

        if options is not None:
            statement = self.options(statement, options)

        result = (await db.execute(statement, **kwargs)).unique().scalar_one_or_none()

        if not result:
            return MISSING

        return result

    async def get_by(
        self,
        db: AsyncSession,
        where: dict[str, Any],
        options: list[tuple[str, StrategyOptions]] | None = None,
        **kwargs: Unpack[Kwargs],
    ) -> ModelType | MISSING_TYPE:
        """Get single item by multiple filters."""
        statement = select(self.model)

        if where is not None:
            statement = statement.where(
                *[getattr(self.model, k) == v for k, v in where.items()],
            )

        if options is not None:
            statement = self.options(statement, options)

        result = (await db.execute(statement, **kwargs)).unique().scalar_one_or_none()

        if not result:
            return MISSING

        return result

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        where: dict[str, Any] | None = None,
        page: int = 0,
        shows: int = 100,
        ordering: list[tuple[str, bool]] | None = None,
        options: list[tuple[str, StrategyOptions]] | None = None,
        complex_filters: list[FilterTypes] | None = None,
        **kwargs: Unpack[Kwargs],
    ) -> tuple[list[ModelType] | EMPTY_TYPE, int]:
        """Get multiple items."""
        statement = select(self.model)

        if where is not None:
            statement = statement.where(
                *[getattr(self.model, k) == v for k, v in where.items()],
            )

        if complex_filters is not None:
            statement = self.apply_filters(complex_filters, statement)

        if ordering is None:
            ordering = [("date_added", True)]

        if options is not None:
            statement = self.options(statement, options)

        ordered = cast("Select[tuple[ModelType]]", self.order_by(statement, ordering))
        paginated = ordered.offset(page).limit(shows)

        count = await self.count(db, statement)
        results = (await db.execute(paginated, **kwargs)).unique().scalars().all()

        return results or EMPTY, count

    async def create(
        self,
        db: AsyncSession,
        *,
        obj_in: CreateSchema | dict[str, Any],
        commit: bool = True,
        options: list[tuple[str, StrategyOptions]] | None = None,
        exclude: set[str] | None = None,
    ) -> ModelType:
        """Insert item."""
        if isinstance(obj_in, dict) is False:
            obj_in: dict[str, Any] = obj_in.model_dump(mode="python", exclude=exclude)

        obj_in = cast("dict[str, Any]", obj_in)  # Redefinition because of type hinting
        stmt = insert(self.model).values(**obj_in).returning(self.model.id)

        with catch_sqlalchemy_exception():
            obj_id = cast("int", (await db.execute(stmt)).unique().scalar_one())

            if commit:
                await db.commit()

        return await self.get(db, obj_id, options)

    async def create_many(
        self,
        db: AsyncSession,
        *,
        objs_in: list[CreateSchema],
        commit: bool = True,
    ) -> list[ModelType]:
        """Insert many items."""
        objs_in_data = [obj_in.model_dump(mode="python") for obj_in in objs_in]
        stmnt = (
            insert(self.model)
            .values([{**obj_data} for obj_data in objs_in_data])
            .returning(self.model.id)
        )

        with catch_sqlalchemy_exception():
            ids = (await db.execute(stmnt)).unique().scalars().all()

            if commit:
                await db.commit()

        return ids

    async def update(
        self,
        db: AsyncSession,
        db_obj_id: int,
        obj_in: UpdateSchema | dict[str, Any],
        commit: bool = True,
        options: list[tuple[str, StrategyOptions]] | None = None,
    ) -> ModelType:
        """Update an item."""
        if isinstance(obj_in, dict) is False:
            obj_in: dict[str, Any] = obj_in.model_dump(mode="json", exclude_unset=True)

        update_data = cast(
            "dict[str, Any]", obj_in
        )  # Redefinition because of type hinting
        stmt = (
            sql_update(self.model)
            .where(self.model.id == db_obj_id)
            .values(**update_data)
            .returning(self.model.id)
        )

        with catch_sqlalchemy_exception():
            obj_id = (await db.execute(stmt)).scalar_one()

            if commit:
                await db.commit()

        return await self.get(db, obj_id, options)

    async def delete(
        self, db: AsyncSession, db_object: ModelType, *, commit: bool = True
    ) -> ModelType:
        with catch_sqlalchemy_exception():
            deleted = await db.delete(db_object)

            if commit:
                await db.commit()

        return deleted

    async def delete_many(
        self, db: AsyncSession, ids: list[int], *, commit: bool = True
    ) -> list[int]:
        stmnt = (
            sql_delete(self.model)
            .where(self.model.id.in_(ids))
            .returning(self.model.id)
        )

        with catch_sqlalchemy_exception():
            deleted = (await db.execute(stmnt)).scalars().all()

            if commit:
                await db.commit()

        return deleted

    async def count(self, db: AsyncSession, statement: Select) -> int | None:
        """Count the number of rows."""
        count_statement = statement.with_only_columns(
            sql_func.count(),
            maintain_column_froms=True,
        ).order_by(None)

        return (await db.execute(count_statement)).scalar_one_or_none()

    def apply_filters(
        self, filters: list[FilterTypes], statement: Select[ModelType]
    ) -> Select[ModelType]:
        """Apply filters to the statement."""
        for filter_ in filters:
            if isinstance(filter_, DateAdded) and filter_.date_added is not None:
                statement = statement.where(
                    sql_func.date(self.model.date_added) == filter_.date_added
                )
            elif isinstance(filter_, Before) and filter_.date_added is not None:
                statement = statement.where(
                    sql_func.date(self.model.date_added) < filter_.date_added
                )
            elif isinstance(filter_, After) and filter_.date_added is not None:
                statement = statement.where(
                    sql_func.date(self.model.date_added) > filter_.date_added
                )
            elif isinstance(filter_, BeforeAfter) and (
                filter_.date_after is not None and filter_.date_before is not None
            ):
                statement = statement.where(
                    sql_func.date(self.model.date_added) >= filter_.date_after,
                    sql_func.date(self.model.date_added) <= filter_.date_before,
                )
            elif isinstance(filter_, Search) and filter_.field_name is not None:
                attr = cast(
                    "InstrumentedAttribute", getattr(self.model, filter_.field_name)
                )
                statement = statement.where(attr.ilike(f"%{filter_.value}%"))
            elif (
                isinstance(filter_, FieldFilter)
                and filter_.field is not None
                and filter_.value is not None
            ):
                attr = cast("InstrumentedAttribute", getattr(self.model, filter_.field))
                statement = statement.where(attr == filter_.value)
            elif isinstance(filter_, MonthlyFilter) and filter_.month is not None:
                attr = cast(
                    "InstrumentedAttribute",
                    getattr(self.model, filter_.field_name or "date_added", None),
                )
                statement = statement.where(
                    sql_func.date_trunc("MONTH", attr)
                    == sql_func.date_trunc("MONTH", filter_.month),
                )
            elif isinstance(filter_, AnyFieldFilter) and filter_.any_value is not None:
                statement = self.any_filter()

        return statement

    def order_by(
        self,
        statement: Select,
        ordering: list[tuple[str, bool]] | OrderBy | None = None,
    ) -> Select:
        """Order by given ordering."""
        if not ordering:
            return statement

        if isinstance(ordering, OrderBy):
            field = cast(
                "InstrumentedAttribute", getattr(self.model, ordering.order_by)
            )
            return statement.order_by(
                desc(field) if ordering.sort_by == "descending" else asc(field)
            )

        for attr, is_desc in ordering:
            try:
                field = cast("InstrumentedAttribute", getattr(self.model, attr))

                if (
                    isinstance(field.prop, RelationshipProperty)
                    and field.prop.lazy != "joined"
                ):
                    statement = statement.join(field)

                statement = statement.order_by(desc(field) if is_desc else asc(field))
            except AttributeError as e:
                # NOTE: Handle this error better.
                raise Exception from e

        return statement

    def options(
        self,
        statement: Select,
        options: list[tuple[str, StrategyOptions]] | None = None,
    ) -> Select:
        """Apply strategy options (e.g joinedload, eagerload) to the statement."""
        if not options:
            return statement

        for attr, strat_op in options:
            try:
                field = cast("InstrumentedAttribute", getattr(self.model, attr))

                statement = statement.options(
                    getattr(strategy_options, strat_op)(field)
                )
            except AttributeError as e:
                raise Exception from e

        return statement
