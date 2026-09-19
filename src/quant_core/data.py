"""Data loading and deterministic sample-data helpers."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class PriceLoadResult:
    """Successful price frames and per-ticker errors from a data request."""

    prices: dict[str, pd.DataFrame]
    errors: dict[str, str]


def validate_prices(prices: pd.DataFrame) -> pd.DataFrame:
    """Return a validated copy of a single-asset close-price frame.

    The engine deliberately accepts a narrow schema at first. A multi-asset schema is
    introduced with the factor-research milestone instead of being prematurely hidden
    behind a generic data abstraction.
    """

    if "close" not in prices.columns:
        raise ValueError("prices must contain a 'close' column")
    if prices.empty:
        raise ValueError("prices must not be empty")
    if not isinstance(prices.index, pd.DatetimeIndex):
        raise TypeError("prices must use a DatetimeIndex")
    if prices.index.has_duplicates:
        raise ValueError("prices index must not contain duplicate dates")
    if not prices.index.is_monotonic_increasing:
        raise ValueError("prices index must be sorted in ascending order")

    result = prices.loc[:, ["close"]].astype(float).copy()
    if result["close"].isna().any():
        raise ValueError("close prices must not contain missing values")
    if (result["close"] <= 0).any():
        raise ValueError("close prices must be positive")
    return result


def generate_sample_prices(
    periods: int = 756,
    *,
    start: str = "2022-01-03",
    initial_price: float = 100.0,
    annual_return: float = 0.08,
    annual_volatility: float = 0.20,
    seed: int = 7,
) -> pd.DataFrame:
    """Generate a reproducible geometric-Brownian-motion price series."""

    if periods < 2:
        raise ValueError("periods must be at least 2")
    if initial_price <= 0:
        raise ValueError("initial_price must be positive")
    if annual_volatility < 0:
        raise ValueError("annual_volatility must be non-negative")

    rng = np.random.default_rng(seed)
    daily_drift = (annual_return - 0.5 * annual_volatility**2) / 252
    daily_volatility = annual_volatility / np.sqrt(252)
    log_returns = rng.normal(daily_drift, daily_volatility, periods - 1)
    values = np.concatenate(([initial_price], initial_price * np.exp(np.cumsum(log_returns))))
    index = pd.bdate_range(start=start, periods=periods)
    return pd.DataFrame({"close": values}, index=index)


def normalize_tickers(tickers: list[str] | tuple[str, ...]) -> list[str]:
    """Trim, uppercase, de-duplicate, and validate user-entered ticker symbols."""

    normalized: list[str] = []
    for raw_ticker in tickers:
        ticker = raw_ticker.strip().upper()
        if not ticker:
            continue
        if len(ticker) > 20:
            raise ValueError(f"ticker is unexpectedly long: {ticker}")
        if ticker not in normalized:
            normalized.append(ticker)
    if not normalized:
        raise ValueError("select at least one ticker")
    return normalized


def generate_sample_universe(
    tickers: list[str] | tuple[str, ...],
    *,
    periods: int = 756,
    seed: int = 7,
) -> dict[str, pd.DataFrame]:
    """Generate independent, reproducible sample prices for several ticker labels."""

    universe: dict[str, pd.DataFrame] = {}
    for ticker in normalize_tickers(tickers):
        digest = sha256(f"{seed}:{ticker}".encode()).digest()
        ticker_seed = int.from_bytes(digest[:4], "big")
        universe[ticker] = generate_sample_prices(periods=periods, seed=ticker_seed)
    return universe


def _extract_close(raw: pd.DataFrame, ticker: str) -> pd.DataFrame:
    if raw.empty:
        raise ValueError("provider returned no rows")

    if isinstance(raw.columns, pd.MultiIndex):
        close_data: pd.Series | pd.DataFrame | None = None
        for level in range(raw.columns.nlevels):
            if "Close" in raw.columns.get_level_values(level):
                close_data = raw.xs("Close", axis=1, level=level)
                break
        if close_data is None:
            raise ValueError("provider response has no Close column")
        close = close_data.iloc[:, 0] if isinstance(close_data, pd.DataFrame) else close_data
    else:
        if "Close" not in raw.columns:
            raise ValueError("provider response has no Close column")
        close = raw["Close"]
        if isinstance(close, pd.DataFrame):
            close = close.iloc[:, 0]

    index = pd.DatetimeIndex(close.index)
    if index.tz is not None:
        index = index.tz_convert(None)
    prices = pd.DataFrame({"close": close.to_numpy()}, index=index)
    prices.index.name = "date"
    try:
        return validate_prices(prices)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"invalid prices for {ticker}: {exc}") from exc


def download_yfinance_prices(
    tickers: list[str] | tuple[str, ...],
    *,
    period: str = "5y",
) -> PriceLoadResult:
    """Download adjusted daily closes while preserving partial successes."""

    try:
        import yfinance as yf
    except ImportError as exc:  # pragma: no cover - dependency is part of the app install
        raise RuntimeError("install yfinance to use market data") from exc

    prices: dict[str, pd.DataFrame] = {}
    errors: dict[str, str] = {}
    for ticker in normalize_tickers(tickers):
        try:
            raw = yf.download(
                ticker,
                period=period,
                auto_adjust=True,
                progress=False,
                threads=False,
            )
            prices[ticker] = _extract_close(raw, ticker)
        except Exception as exc:
            errors[ticker] = str(exc)
    return PriceLoadResult(prices=prices, errors=errors)
