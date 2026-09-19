"""The strategy plug-in contract and parameter metadata."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import MISSING, Field, dataclass, field, fields, is_dataclass
from typing import Any, ClassVar

import pandas as pd

_UI_METADATA_KEY = "strategy_ui"


@dataclass(frozen=True)
class StrategyParameter:
    """UI-agnostic metadata describing one configurable strategy field."""

    name: str
    label: str
    default: int | float | bool | str
    value_type: type
    min_value: int | float | None = None
    max_value: int | float | None = None
    step: int | float | None = None
    help: str | None = None


def strategy_parameter(
    default: int | float | bool | str,
    *,
    label: str,
    min_value: int | float | None = None,
    max_value: int | float | None = None,
    step: int | float | None = None,
    help: str | None = None,
) -> Field[Any]:
    """Declare a dataclass field that the UI can configure automatically."""

    return field(
        default=default,
        metadata={
            _UI_METADATA_KEY: {
                "label": label,
                "min_value": min_value,
                "max_value": max_value,
                "step": step,
                "help": help,
            }
        },
    )


class Strategy(ABC):
    """Base class implemented by every trusted local strategy plug-in."""

    strategy_id: ClassVar[str]
    display_name: ClassVar[str]
    description: ClassVar[str] = ""

    @property
    def name(self) -> str:
        configured = ", ".join(f"{item.name}={getattr(self, item.name)}" for item in fields(self))
        return f"{self.display_name} ({configured})" if configured else self.display_name

    @abstractmethod
    def generate_targets(self, prices: pd.DataFrame) -> pd.Series:
        """Return targets in [-1, 1] using information available at each row's close."""


def strategy_parameters(strategy_type: type[Strategy]) -> list[StrategyParameter]:
    """Extract configurable parameters from a strategy dataclass."""

    if not is_dataclass(strategy_type):
        raise TypeError(f"{strategy_type.__name__} must be a dataclass")

    parameters: list[StrategyParameter] = []
    for item in fields(strategy_type):
        if item.default is MISSING:
            raise TypeError(f"strategy field '{item.name}' must have a default value")
        metadata = item.metadata.get(_UI_METADATA_KEY, {})
        parameters.append(
            StrategyParameter(
                name=item.name,
                label=metadata.get("label", item.name.replace("_", " ").capitalize()),
                default=item.default,
                value_type=type(item.default),
                min_value=metadata.get("min_value"),
                max_value=metadata.get("max_value"),
                step=metadata.get("step"),
                help=metadata.get("help"),
            )
        )
    return parameters
