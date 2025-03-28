from src.core.schema import BaseModel


class TransactionType(BaseModel):
    name: str | None = None


class TransactionTypeCreate(TransactionType):
    name: str


class TransactionTypeUpdate(TransactionType):
    name: str


class TransactionTypeResponse(TransactionType):
    id: int
