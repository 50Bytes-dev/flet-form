import asyncio
from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Sequence, Union, cast
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    CrossAxisAlignment,
    MainAxisAlignment,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    ScrollMode,
)
from flet import (
    Column,
    MainAxisAlignment,
    CrossAxisAlignment,
)
from flet_form.types import (
    AnyContainerOrControl,
    ControlsContainer,
    ContentContainer,
)
from flet_form.input import FormInput


@dataclass
class ValidationCompleteEvent:
    valid: bool


ValidationCompleteHandler = Callable[[ValidationCompleteEvent], None]


class Form(Column):

    def __init__(
        self,
        controls: Optional[List[Control]] = None,
        lazy: bool = False,
        on_validation_complete: Optional[ValidationCompleteHandler] = None,
        #
        # Column
        #
        alignment: MainAxisAlignment = MainAxisAlignment.NONE,
        horizontal_alignment: CrossAxisAlignment = CrossAxisAlignment.NONE,
        spacing: OptionalNumber = None,
        tight: Optional[bool] = None,
        wrap: Optional[bool] = None,
        run_spacing: OptionalNumber = None,
        #
        # ConstrainedControl
        #
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        expand_loose: Optional[bool] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        rotate: RotateValue = None,
        scale: ScaleValue = None,
        offset: OffsetValue = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: AnimationValue = None,
        animate_size: AnimationValue = None,
        animate_position: AnimationValue = None,
        animate_rotation: AnimationValue = None,
        animate_scale: AnimationValue = None,
        animate_offset: AnimationValue = None,
        on_animation_end=None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        rtl: Optional[bool] = None,
        #
        # ScrollableControl and AdaptiveControl
        #
        scroll: Optional[ScrollMode] = None,
        auto_scroll: Optional[bool] = None,
        on_scroll_interval: OptionalNumber = None,
        on_scroll: Any = None,
        adaptive: Optional[bool] = None,
    ):
        super().__init__(
            controls=controls,
            alignment=alignment,
            horizontal_alignment=horizontal_alignment,
            spacing=spacing,
            tight=tight,
            wrap=wrap,
            run_spacing=run_spacing,
            ref=ref,
            key=key,
            width=width,
            height=height,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            expand=expand,
            expand_loose=expand_loose,
            col=col,
            opacity=opacity,
            rotate=rotate,
            scale=scale,
            offset=offset,
            aspect_ratio=aspect_ratio,
            animate_opacity=animate_opacity,
            animate_size=animate_size,
            animate_position=animate_position,
            animate_rotation=animate_rotation,
            animate_scale=animate_scale,
            animate_offset=animate_offset,
            on_animation_end=on_animation_end,
            visible=visible,
            disabled=disabled,
            data=data,
            rtl=rtl,
            scroll=scroll,
            auto_scroll=auto_scroll,
            on_scroll_interval=on_scroll_interval,
            on_scroll=on_scroll,
            adaptive=adaptive,
        )

        self.lazy = lazy
        self.inputs: List[FormInput] = self._prepare_inputs(controls)
        self.on_validation_complete = on_validation_complete

    async def validate(self):
        valid = True
        for input in self.inputs:
            if not input.validate():
                valid = False
                break

        if self.on_validation_complete is not None and self.page is not None:
            event = ValidationCompleteEvent(valid=valid)
            if asyncio.iscoroutinefunction(self.on_validation_complete):
                await self.on_validation_complete(event)
            else:
                self.on_validation_complete(event)

        return valid

    def _isinput(
        self,
        control: Control,
    ) -> bool:
        return isinstance(control, FormInput)

    def _prepare_inputs(
        self,
        controls: Optional[Sequence[AnyContainerOrControl]],
    ):
        inputs = []

        if controls is None:
            return inputs

        for control in controls:
            if isinstance(control, Control):
                if self._isinput(control):
                    cast(FormInput, control).attach_form(self)
                    inputs.append(control)
            elif isinstance(control, ContentContainer) and control.content is not None:
                control_inputs = self._prepare_inputs([control.content])
                inputs.extend(control_inputs)
            elif isinstance(control, ControlsContainer):
                contol_inputs = self._prepare_inputs(control.controls)
                inputs.extend(contol_inputs)

        return inputs

    @property
    def on_validation_complete(self):
        return self._get_event_handler("validation_complete")

    @on_validation_complete.setter
    def on_validation_complete(self, handler):
        self._add_event_handler("validation_complete", handler)
