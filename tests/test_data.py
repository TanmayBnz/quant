import pandas as pd
import pytest

from quant_core.data import (
    generate_sample_prices,
    generate_sample_universe,
    normalize_tickers,
    validate_prices,
)


def test_sample_prices_are_reproducible() -> None:
    first = generate_sample_prices(periods=10, seed=42)
    second = generate_sample_prices(periods=10, seed=42)
    pd.testing.assert_frame_equal(first, second)


def test_validate_prices_rejects_unsorted_index() -> None:
    prices = pd.DataFrame(
        {"close": [100.0, 101.0]},
        index=pd.to_datetime(["2024-01-03", "2024-01-02"]),
    )
    with pytest.raises(ValueError, match="sorted"):
        validate_prices(prices)


def test_sample_universe_is_stable_and_distinct() -> None:
    first = generate_sample_universe(["aapl", "MSFT"], periods=10, seed=3)
    second = generate_sample_universe(["AAPL", "msft"], periods=10, seed=3)
    assert list(first) == ["AAPL", "MSFT"]
    pd.testing.assert_frame_equal(first["AAPL"], second["AAPL"])
    assert not first["AAPL"].equals(first["MSFT"])


def test_normalize_tickers_removes_duplicates() -> None:
    assert normalize_tickers([" aapl ", "AAPL", "msft"]) == ["AAPL", "MSFT"]
