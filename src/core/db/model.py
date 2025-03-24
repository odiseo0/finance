from __future__ import annotations

import dataclasses
from collections.abc import Awaitable
from datetime import datetime
from typing import Any, TypeVar

from sqlalchemy import DateTime, MetaData, func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import registry as _registry
from sqlalchemy.util import greenlet_spawn

from src.core.utils import datetime_now, pluralize
from src.core.utils.helpers import to_snake


_T = TypeVar("_T", bound=Any)
meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    },
)


class AwaitAttrs:
    """
    AwaitAttrs provides an alternative solution for accessing lazy-loaded SQLAlchemy attributes in async code.

    BACKGROUND:
    When using SQLAlchemy with asyncio, direct access to lazy-loaded relationships
    causes exceptions because it would trigger implicit database IO.

    RECOMMENDED APPROACHES:
    SQLAlchemy officially recommends these approaches which should be preferred in most cases:
    - Eagerly load relationships with joinedload() or selectinload() (best practice)
    - Use session.run_sync() to access the attribute in a sync context
    - Use session.refresh() to explicitly load the attribute

    ALTERNATIVE SOLUTION:
    AwaitAttrs is an unofficial approach that allows lazy attributes to be awaited.
    While not recommended for general use, it may be helpful in specific scenarios
    where the standard approaches are impractical.

    USAGE:
    With this mixin, you can access lazy-loaded relationships in two ways:

    1. Using await_attr property:
    related_items = await model_instance.await_attr.relationship_name

    2. Using await_load method (with typing support):
    related_items = await model_instance.await_load(ModelClass.relationship_name)

    NOTE: The SQLAlchemy documentation explicitly recommends eager loading as the
    preferred solution for handling relationships in async code, and this approach
    should only be used when necessary.

    For more information, see:
    https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#preventing-implicit-io-when-using-asyncsession
    https://github.com/sqlalchemy/sqlalchemy/discussions/9731
    https://docs.sqlalchemy.org/en/20/_modules/examples/asyncio/async_orm.html
    """

    class _AwaitAttrGetitem:
        __slots__ = ("_instance",)

        def __init__(self, _instance: Any):
            self._instance = _instance

        def __getattr__(self, name: str) -> Awaitable[Any]:
            return greenlet_spawn(getattr, self._instance, name)

    @property
    def await_attr(self) -> AwaitAttrs._AwaitAttrGetitem:
        """provide awaitable attribute access"""
        return AwaitAttrs._AwaitAttrGetitem(self)

    async def await_load(self, attr: Mapped[_T]) -> _T:
        """typed version of getattr"""
        return await greenlet_spawn(
            getattr,
            self,
            attr.key,
        )


class Base(AwaitAttrs, DeclarativeBase):
    """subclasses will be converted to dataclasses"""

    metadata = meta
    registry = _registry(type_annotation_map={datetime: DateTime(timezone=True)})

    @declared_attr
    @classmethod
    def __tablename__(cls) -> str:
        return pluralize(to_snake(cls.__name__))


@dataclasses.dataclass
class Date:
    date_added: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default_factory=datetime_now,
        server_default=func.now(),
    )
    date_updated: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        onupdate=datetime_now,
    )
