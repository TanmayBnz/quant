import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

TICKER = "AAPL"

N_days = 1000

FAST_WINDOW = 20
SLOW_WINDOW = 60
INITIAL_CAPITAL = 100.0
RISK_FREE_RATE = 0.0
PERIODS_PER_YEAR = 252


def load_prices(ticker = None, n_days = 500):
    if ticker:
        try:
            import yfinance as yf
            raw = yf.download(ticker, period="2y", progress=False)
            if isinstance(raw.columns, pd.MultiIndex):
                raw.columns = raw.columns.get_level_values(0)
            df = raw[["Close"]].rename(columns={"Close": "close"})
            return df
        except Exception as e:
            print(f"Error loading data for {ticker}: {e}")
            return None

def moving_average_signal(prices, fast = 10, slow = 30):
    fast_ma = prices['close'].rolling(window=fast).mean()
    slow_ma = prices['close'].rolling(window=slow).mean()
    raw_signal = (fast_ma > slow_ma).astype(int) - (fast_ma < slow_ma).astype(int)
    signal = raw_signal.shift(1).fillna(0)
    return signal

def run_backtest(prices, signal, initial_capital = 100.0):
    df = prices.copy()
    df['signal'] = signal
    df['daily_return'] = df['close'].pct_change().fillna(0)
    df['strategy_return'] = df['signal'] * df['daily_return']
    df['equity'] = initial_capital * (1 + df['strategy_return']).cumprod()
    return df

def extract_trades(df):
    trades = []
    current_position = 0
    entry_price = entry_date = None

    def close_trade(exit_price, exit_date):
        raw_move = (exit_price - entry_price) / entry_price
        return {
            'entry_date': entry_date,
            'exit_date': exit_date,
            'entry_price': entry_price,
            'exit_price': exit_price,
            'direction': 'long' if current_position == 1 else 'short',
            'return_pct': current_position * raw_move
        }

    for record in df.itertuples():
        new_position = record.signal
        if new_position != current_position:
            if current_position != 0:
                trades.append(close_trade(record.close, record.Index))
            if new_position != 0:
                entry_price = record.close
                entry_date = record.Index
            current_position = new_position
    if current_position != 0:
        trades.append(close_trade(df['close'].iloc[-1], df.index[-1]))
    return pd.DataFrame(trades)


def sharpe_ratio(daily_returns, risk_free_rate = 0.0, periods_per_year = 252):
    daily_rf = risk_free_rate / periods_per_year
    excess_returns = daily_returns - daily_rf
    std = excess_returns.std()
    if std == 0:
        return 0.0
    return (excess_returns.mean() / std) * np.sqrt(periods_per_year)

def max_drawdown(equity_curve):
    running_max = equity_curve.cummax()
    drawdown_series = equity_curve / running_max - 1
    return drawdown_series.min(), drawdown_series.idxmin()

def win_rate(trades_df):
    if len(trades_df) == 0:
        return 0.0
    wins = (trades_df['return_pct'] > 0).sum()
    return wins / len(trades_df)


def summarize(df, trades_df):
    sharpe = sharpe_ratio(df['strategy_return'], RISK_FREE_RATE, PERIODS_PER_YEAR)
    mdd, dd_series = max_drawdown(df['equity'])
    wr = win_rate(trades_df)
    total_return = df['equity'].iloc[-1] / df['equity'].iloc[0] - 1
    print("BACKTEST SUMMARY")
    print(f"period: {df.index[0].date()} to {df.index[-1].date()}")
    print(f"total return: {total_return:.2%}")
    print(f"sharpe ratio: {sharpe:.2f}")
    print(f"max drawdown: {mdd:.2%}")
    print(f"win rate: {wr:.2%}")

    return {
        "total_return": total_return,
        "sharpe_ratio": sharpe,
        "max_drawdown": mdd,
        "win_rate": wr,
        "drawdown_series": dd_series
    }


if __name__ == "__main__":
    prices = load_prices(TICKER, N_days)
    signal = moving_average_signal(prices, FAST_WINDOW, SLOW_WINDOW)
    results_df = run_backtest(prices, signal, INITIAL_CAPITAL)
    trades_df = extract_trades(results_df)
    summary = summarize(results_df, trades_df)

    if len(trades_df) > 0:
        print("\nFirst few trades")
        print(trades_df.head().to_string(index=False))
