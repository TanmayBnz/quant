"""Discovery for trusted strategy files stored outside the engine package."""

from __future__ import annotations

import importlib.util
import inspect
import sys
from pathlib import Path

from quant_core.strategies import Strategy, strategy_parameters


class StrategyLoadError(RuntimeError):
    """Raised when a local strategy module does not satisfy the plug-in contract."""


def discover_strategy_classes(directory: Path) -> dict[str, type[Strategy]]:
    """Load strategy subclasses from each public Python file in ``directory``.

    Strategy files are executable Python and are therefore treated as trusted local
    code. Files whose names begin with an underscore are ignored, which lets the folder
    contain helpers and a copyable template.
    """

    if not directory.is_dir():
        raise StrategyLoadError(f"strategy directory does not exist: {directory}")

    discovered: dict[str, type[Strategy]] = {}
    for path in sorted(directory.glob("*.py")):
        if path.name.startswith("_"):
            continue

        module_name = f"_quant_local_strategy_{path.stem}"
        module_spec = importlib.util.spec_from_file_location(module_name, path)
        if module_spec is None or module_spec.loader is None:
            raise StrategyLoadError(f"could not create an import spec for {path.name}")

        module = importlib.util.module_from_spec(module_spec)
        sys.modules[module_name] = module
        try:
            module_spec.loader.exec_module(module)
        except Exception as exc:
            raise StrategyLoadError(f"could not load {path.name}: {exc}") from exc

        for _, candidate in inspect.getmembers(module, inspect.isclass):
            if candidate is Strategy or not issubclass(candidate, Strategy):
                continue
            if candidate.__module__ != module.__name__:
                continue
            if not getattr(candidate, "strategy_id", ""):
                raise StrategyLoadError(f"{candidate.__name__} must define strategy_id")
            if not getattr(candidate, "display_name", ""):
                raise StrategyLoadError(f"{candidate.__name__} must define display_name")
            strategy_parameters(candidate)
            if candidate.strategy_id in discovered:
                raise StrategyLoadError(f"duplicate strategy_id: {candidate.strategy_id}")
            discovered[candidate.strategy_id] = candidate

    if not discovered:
        raise StrategyLoadError(f"no strategy classes found in {directory}")
    return discovered
