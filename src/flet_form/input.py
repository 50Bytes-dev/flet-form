from abc import abstractproperty
import asyncio
from typing import TYPE_CHECKING, Generic, List, Optional, TypeVar
from flet import Page
from flet_form.types import RuleCallable

T = TypeVar("T")

FormInputRules = Optional[List[RuleCallable[T]]]

if TYPE_CHECKING:
    from flet_form.form import Form


class FormInput(Generic[T]):
    def __init__(
        self,
        rules: FormInputRules = None,
    ):
        self.form: Optional["Form"] = None
        self.rules = rules

    @abstractproperty
    def _value_for_validation(self) -> T: ...

    def validate(self) -> bool:
        if self.rules:
            for rule in self.rules:
                if not rule(self._value_for_validation):
                    return False
        return True

    async def _on_change_validate(self):
        if self.form is not None:
            await self.form.validate()

    def _get_on_change_handler(self, default_handler):

        async def _on_change_handler(e):
            if default_handler is not None:
                if asyncio.iscoroutinefunction(default_handler):
                    await default_handler(e)
                else:
                    default_handler(e)
            if self.form and not self.form.lazy:
                await self._on_change_validate()

        if default_handler is None and self.form and self.form.lazy:
            return None

        return _on_change_handler

    def attach_form(self, form: "Form"):
        self.form = form
        self.on_change = self._get_on_change_handler(self.on_change)
