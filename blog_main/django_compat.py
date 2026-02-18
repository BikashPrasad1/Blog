"""Runtime compatibility patches for unsupported interpreter combos."""

from copy import copy

from django.template.context import BaseContext


def patch_base_context_copy() -> None:
    """
    Work around Python 3.14 behavior that breaks Django 4.2 BaseContext.__copy__.
    """

    original_copy = BaseContext.__copy__

    def _safe_copy(self):
        try:
            return original_copy(self)
        except AttributeError:
            duplicate = object.__new__(self.__class__)
            duplicate.__dict__.update(self.__dict__)
            duplicate.dicts = self.dicts[:]
            return duplicate

    BaseContext.__copy__ = _safe_copy


patch_base_context_copy()
