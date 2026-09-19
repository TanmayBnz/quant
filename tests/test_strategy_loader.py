from pathlib import Path

from quant_core.strategy_loader import discover_strategy_classes


def test_discovers_public_strategy_files() -> None:
    strategies = discover_strategy_classes(Path("strategies"))
    assert set(strategies) == {"buy_and_hold", "moving_average", "rsi_mean_reversion"}
    assert strategies["moving_average"].display_name == "Moving-average crossover"
