from litestar import Router

from .infrastructure import (
    add_transaction,
    add_transaction_file,
    add_transaction_type,
    edit_transaction,
    edit_transaction_file,
    edit_transaction_type,
    eliminate_transaction,
    eliminate_transaction_file,
    eliminate_transaction_type,
    read_multi_transaction_files,
    read_multi_transaction_types,
    read_multi_transactions,
    read_transaction,
    read_transaction_type,
)


api = Router(
    path="/transactions",
    tags=["Transactions"],
    route_handlers=[
        read_multi_transaction_types,
        read_transaction_type,
        add_transaction_type,
        edit_transaction_type,
        eliminate_transaction_type,
        read_transaction,
        read_multi_transactions,
        add_transaction,
        edit_transaction,
        eliminate_transaction,
        add_transaction_file,
        edit_transaction_file,
        eliminate_transaction_file,
        read_multi_transaction_files,
    ],
)
