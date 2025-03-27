from contextlib import contextmanager
from typing import Optional

from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError


class DatabaseError(Exception):
    """Base exception for database-related errors."""

    def __init__(self, message: str, original_error: Optional[Exception] = None):
        self.original_error = original_error
        super().__init__(message)


class DatabaseConnectionError(DatabaseError):
    """Raised when there's an issue connecting to the database."""

    pass


class DatabaseConstraintError(DatabaseError):
    """Raised when a database constraint is violated."""

    pass


class DatabaseQueryError(DatabaseError):
    """Raised when there's an error in the query syntax or execution."""

    pass


class DatabaseTimeoutError(DatabaseError):
    """Raised when a database operation times out."""

    pass


class DatabaseDataError(DatabaseError):
    """Raised when there's an issue with the data being processed."""

    pass


@contextmanager
def catch_sqlalchemy_exception(operation_name: str = "database operation"):
    """
    Context manager to handle common SQLAlchemy exceptions with detailed error messages.
    Uses pattern matching to handle different types of database errors.
    """
    try:
        yield
    except IntegrityError as e:
        error_msg = str(e.orig) if hasattr(e, "orig") else str(e)

        match error_msg.lower():
            case msg if "unique constraint" in msg:
                raise DatabaseConstraintError(
                    f"Unique constraint violation while {operation_name}: {error_msg}",
                    original_error=e,
                )
            case msg if "foreign key constraint" in msg:
                raise DatabaseConstraintError(
                    f"Foreign key constraint violation while {operation_name}: {error_msg}",
                    original_error=e,
                )
            case msg if "not null constraint" in msg:
                raise DatabaseConstraintError(
                    f"Not null constraint violation while {operation_name}: {error_msg}",
                    original_error=e,
                )
            case msg if "check constraint" in msg:
                raise DatabaseConstraintError(
                    f"Check constraint violation while {operation_name}: {error_msg}",
                    original_error=e,
                )
            case _:
                raise DatabaseConstraintError(
                    f"Constraint violation while {operation_name}: {error_msg}",
                    original_error=e,
                )
    except OperationalError as e:
        match str(e).lower():
            case msg if "connection" in msg:
                raise DatabaseConnectionError(
                    f"Database connection error while {operation_name}: {str(e)}",
                    original_error=e,
                )
            case msg if "timeout" in msg:
                raise DatabaseConnectionError(
                    f"Connection timeout while {operation_name}: {str(e)}",
                    original_error=e,
                )
            case msg if "deadlock" in msg:
                raise DatabaseConnectionError(
                    f"Deadlock detected while {operation_name}: {str(e)}",
                    original_error=e,
                )
            case msg if "server closed" in msg:
                raise DatabaseConnectionError(
                    f"Server connection closed while {operation_name}: {str(e)}",
                    original_error=e,
                )
            case _:
                raise DatabaseConnectionError(
                    f"Database operational error while {operation_name}: {str(e)}",
                    original_error=e,
                )
    except SQLAlchemyError as e:
        match str(e).lower():
            case msg if "expired" in msg:
                raise DatabaseError(
                    f"Session expired while {operation_name}: {str(e)}",
                    original_error=e,
                )
            case msg if "already attached" in msg:
                raise DatabaseError(
                    f"Object already attached to session while {operation_name}: {str(e)}",
                    original_error=e,
                )
            case msg if "rollback" in msg:
                raise DatabaseError(
                    f"Transaction rollback error while {operation_name}: {str(e)}",
                    original_error=e,
                )
            case msg if "commit" in msg:
                raise DatabaseError(
                    f"Transaction commit error while {operation_name}: {str(e)}",
                    original_error=e,
                )
            case _:
                raise DatabaseError(
                    f"Unexpected database error while {operation_name}: {str(e)}",
                    original_error=e,
                )
