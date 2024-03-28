from abc import ABC, abstractmethod
from typing import (
    TYPE_CHECKING,
    TypeVar,
    Callable,
    List,
    Optional,
    Union,
    Protocol,
    runtime_checkable,
)
from flet_core import Control

if TYPE_CHECKING:
    from flet_form.form import Form

T = TypeVar("T")

RuleCallable = Callable[[T], bool]


@runtime_checkable
class ControlsContainer(Protocol):
    controls: Optional[List["AnyContainerOrControl"]]


@runtime_checkable
class ContentContainer(Protocol):
    content: Optional["AnyContainerOrControl"]


AnyContainerOrControl = Union[ControlsContainer, ContentContainer, Control]
