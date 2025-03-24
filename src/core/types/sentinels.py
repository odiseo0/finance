# Implementation of Sentinel values based on PEP 661.
#
# PEP 661 Summary:
# - Sentinels are unique placeholder values used for default arguments, missing values, etc.
# - While Python has None, sometimes distinct sentinel values are needed (when None is valid).
# - A good sentinel implementation should:
#   1. Have a clear, informative repr
#   2. Support proper type hinting
#   3. Maintain identity after pickling/copying
#   4. Be simple to create and use
#
# This module provides a registry-based Sentinel implementation that ensures unique
# sentinel values by name within the module, handles pickling correctly, and
# provides meaningful string representations.
#
# Usage:
# NOT_GIVEN = Sentinel("NOT_GIVEN")
#
# def example(value=NOT_GIVEN):
#     if value is NOT_GIVEN:
#         # Handle case where value wasn't provided
#         ...
# PEP 661 REFERENCE: https://peps.python.org/pep-0661/

import sys
from typing import Any, Type, TypeVar, Union, cast


_registry = {}
_T = TypeVar("_T")


class SentinelMeta(type):
    """
    Metaclass for creating sentinel type classes.

    This allows each sentinel value to have its own distinct type
    for use in type annotations.
    """

    def __new__(mcs, name: str, bases: tuple, namespace: dict) -> type:
        return super().__new__(mcs, name, bases, namespace)


class Sentinel:
    """
    Unique sentinel values.

    Sentinel objects are unique by name within each module and preserve
    their identity after pickling/copying.

    Sentinels are considered truthy in boolean contexts and can be used
    in type annotations like: func(x: int | NOT_GIVEN) -> None
    """

    def __new__(cls, name, module_name=None):
        name = str(name)

        if module_name is None:
            # Get the caller's module name
            frame = sys._getframe(1)
            module_name = frame.f_globals.get("__name__", __name__)

        registry_key = f"{module_name}-{name}"

        sentinel = _registry.get(registry_key, None)
        if sentinel is not None:
            return sentinel

        sentinel = super().__new__(cls)
        sentinel._name = name
        sentinel._module_name = module_name

        return _registry.setdefault(registry_key, sentinel)

    def __repr__(self):
        return self._name

    def __str__(self):
        return self._name

    def __bool__(self):
        # Sentinels are truthy by default (like Ellipsis)
        return True

    def __hash__(self):
        # Is hashing a sentinel value necessary? Sentinels are typically compared by identity (is),
        # not equality (==). However, supporting hash allows sentinels to be used in sets and as
        # dictionary keys, which might be useful in some advanced use cases.
        return hash((self._module_name, self._name))

    def __eq__(self, other):
        # Identity-based equality
        return self is other

    def __or__(self, other):
        # Support for Union types: NOT_GIVEN | int
        return Union[self.__class__, other]

    def __ror__(self, other):
        # Support for Union types: int | NOT_GIVEN
        return Union[other, self.__class__]

    def __reduce__(self):
        # Ensure proper pickling
        return (
            self.__class__,
            (self._name, self._module_name),
        )


MISSING = Sentinel("MISSING")  # to replace `None` values
EMPTY = Sentinel("EMPTY")  # to replace empty strings, lists, etc.
MISSING_TYPE = cast(Type[Any], MISSING.__class__)
EMPTY_TYPE = cast(Type[Any], EMPTY.__class__)
