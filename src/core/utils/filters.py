from dataclasses import dataclass
from datetime import date
from typing import Annotated, Any, Literal, TypeAlias

from litestar.di import Provide
from litestar.params import Dependency, Parameter

from .helpers import to_snake


FILTERS_DEPENDENCY_KEY = "filters"
DATE_ADDED_FILTER_DEPENDENCY_KEY = "date_added_filter"
DATE_AFTER_FILTER_DEPENDENCY_KEY = "date_after_filter"
DATE_BEFORE_FILTER_DEPENDENCY_KEY = "date_before_filter"
BETWEEN_DATES_FILTER_DEPENDENCY_KEY = "between_dates_filter"
PAGINATION_DEPENDENCY_KEY = "pagination"
ORDER_BY_DEPENDENCY_KEY = "order_by_filter"
SEARCH_DEPENDENCY_KEY = "search_filter"
FIELD_FILTER_DEPENDENCY_KEY = "field_filter"
MONTH_FILTER_DEPENDENCY_KEY = "month_filter"
ANY_FILTER_DEPENDENCY_KEY = "any_filter"


@dataclass
class DateAdded:
    date_added: date | None = None


@dataclass
class Before:
    date_added: date | None = None


@dataclass
class After:
    date_added: date | None = None


@dataclass
class BeforeAfter:
    date_before: date | None = None
    date_after: date | None = None


@dataclass
class OrderBy:
    order_by: str | None = None
    sort_by: Literal["descending", "ascending"] = "descending"


@dataclass
class Pagination:
    page: int
    shows: int


@dataclass
class Search:
    field_name: str | None = None
    value: str | None = None


@dataclass
class FieldFilter:
    field: str | None = None
    value: int | str | None = None


@dataclass
class MonthlyFilter:
    field_name: str | None = None
    month: date | None = None


@dataclass
class AnyFieldFilter:
    any_name: str | None = None
    any_value: Any | None = None


FilterTypes: TypeAlias = (
    Before | After | BeforeAfter | DateAdded | Search | FieldFilter | MonthlyFilter
)


def provide_date_added(
    date: Annotated[
        date | None, Parameter(query="dateAdded", default=None, required=False)
    ] = None,
) -> DateAdded:
    return DateAdded(date_added=date)


def provide_before(
    before: Annotated[
        date | None, Parameter(query="createdBefore", default=None, required=False)
    ] = None,
) -> Before:
    return Before(date_added=before)


def provide_after(
    after: Annotated[date | None, Parameter(query="createdAfter")] = None,
) -> After:
    return After(date_added=after)


def provide_before_and_after(
    before: Annotated[
        date | None, Parameter(query="dateBefore", default=None, required=False)
    ] = None,
    after: Annotated[date | None, Parameter(query="dateAfter")] = None,
) -> BeforeAfter:
    return BeforeAfter(date_before=before, date_after=after)


def provide_pagination(
    page: Annotated[int, Parameter(query="page", default=1, required=False)] = 1,
    shows: Annotated[int, Parameter(query="shows", default=20, required=False)] = 20,
) -> Pagination:
    return Pagination(page=page, shows=shows)


def provide_order_by(
    order_by: Annotated[
        str | None, Parameter(query="orderBy", default=None, required=False)
    ] = None,
    sort_by: Annotated[
        Literal["descending", "ascending"],
        Parameter(query="sortBy", default="descending", required=None),
    ] = "descending",
) -> OrderBy:
    if order_by is None:
        return None

    order_by = to_snake(order_by)
    return OrderBy(order_by=order_by, sort_by=sort_by)


def provide_search(
    search_field: Annotated[
        str | None, Parameter(query="searchField", default=None, required=False)
    ] = None,
    search_value: Annotated[
        str | None, Parameter(query="searchValue", default=None, required=False)
    ] = None,
) -> Search:
    if search_field is not None:
        search_field = to_snake(search_field)

    return Search(field_name=search_field, value=search_value)


def provide_field_filter(
    field: Annotated[
        str | None, Parameter(query="field", default=None, required=False)
    ] = None,
    value: Annotated[
        int | str | None, Parameter(query="fieldValue", default=None, required=False)
    ] = None,
) -> FieldFilter:
    if field is not None:
        field = to_snake(field)

    return FieldFilter(
        field=field,
        value=int(value) if value is not None and value.isnumeric() else value,
    )


def provide_monthly_filter(
    field_name: Annotated[
        str | None, Parameter(query="dateField", default=None, required=False)
    ] = None,
    monthly_value: Annotated[
        date | None, Parameter(query="monthlyDate", default=None, required=False)
    ] = None,
) -> MonthlyFilter:
    if field_name is not None:
        field_name = to_snake(field_name)

    return MonthlyFilter(field_name=field_name, month=monthly_value)


def provide_any_field_filter(
    field: Annotated[
        str | None, Parameter(query="anyField", default=None, required=False)
    ] = None,
    any_value: Annotated[
        Any | None, Parameter(query="anyValue", default=None, required=False)
    ] = None,
) -> AnyFieldFilter:
    if field is not None:
        field = to_snake(field)

    return AnyFieldFilter(any_name=field, any_value=any_value)


def provide_filter_dependencies(
    date_before_filter: Before = Dependency(skip_validation=True),  # noqa: B008
    date_after_filter: After = Dependency(skip_validation=True),  # noqa: B008
    between_dates_filter: BeforeAfter = Dependency(skip_validation=True),  # noqa: B008
    search_filter: Search = Dependency(skip_validation=True),  # noqa: B008
) -> list[FilterTypes]:
    filters: list[FilterTypes] = []
    filters.extend([date_before_filter, date_after_filter, between_dates_filter])

    if search_filter.field_name is not None:
        filters.append(search_filter)

    return filters


filter_dependencies = {
    FILTERS_DEPENDENCY_KEY: Provide(provide_filter_dependencies, sync_to_thread=False),
    DATE_ADDED_FILTER_DEPENDENCY_KEY: Provide(provide_date_added, sync_to_thread=False),
    DATE_AFTER_FILTER_DEPENDENCY_KEY: Provide(provide_after, sync_to_thread=False),
    DATE_BEFORE_FILTER_DEPENDENCY_KEY: Provide(provide_before, sync_to_thread=False),
    BETWEEN_DATES_FILTER_DEPENDENCY_KEY: Provide(
        provide_before_and_after, sync_to_thread=False
    ),
    PAGINATION_DEPENDENCY_KEY: Provide(provide_pagination, sync_to_thread=False),
    ORDER_BY_DEPENDENCY_KEY: Provide(provide_order_by, sync_to_thread=False),
    SEARCH_DEPENDENCY_KEY: Provide(provide_search, sync_to_thread=False),
    FIELD_FILTER_DEPENDENCY_KEY: Provide(provide_field_filter, sync_to_thread=False),
    MONTH_FILTER_DEPENDENCY_KEY: Provide(provide_monthly_filter, sync_to_thread=False),
    ANY_FILTER_DEPENDENCY_KEY: Provide(provide_any_field_filter, sync_to_thread=False),
}
