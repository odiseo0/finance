from typing import Any, Literal, TypedDict


StrategyOptions = Literal[
    "contains_eager",
    "defaultload",
    "defer",
    "immediateload",
    "joinedload",
    "lazyload",
    "Load",
    "load_only",
    "noload",
    "raiseload",
    "selectin_polymorphic",
    "selectinload",
    "subqueryload",
    "undefer",
    "undefer_group",
    "with_expression",
]


class KnownExecutionOptions(TypedDict, total=False):
    compiled_cache: dict[str, Literal["compiled"]] | None
    logging_token: str
    isolation_level: Literal[
        "SERIALIZABLE",
        "REPEATABLE READ",
        "READ COMMITTED",
        "READ UNCOMMITTED",
        "AUTOCOMMIT",
    ]
    no_parameters: bool
    stream_results: bool
    max_row_buffer: int
    yield_per: int
    insertmanyvalues_page_size: int
    schema_translate_map: dict[str | None, str | None] | None
    populate_existing: bool
    autoflush: bool
    synchronize_session: Literal[False, "auto", "evaluate", "fetch"]
    dml_strategy: Literal["bulk", "raw", "orm", "auto"]
    is_delete_using: bool
    is_update_from: bool
    render_nulls: bool


class Kwargs(TypedDict, total=False):
    bind_arguments: dict[str, Any]
    execution_options: KnownExecutionOptions
