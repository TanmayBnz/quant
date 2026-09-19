from streamlit.testing.v1 import AppTest


def test_backtester_renders_three_ticker_comparison() -> None:
    app = AppTest.from_file("../apps/backtester/app.py", default_timeout=15).run()

    assert not app.exception
    assert len(app.dataframe[0].value) == 3
    assert set(app.dataframe[0].value["ticker"]) == {"AAPL", "MSFT", "NVDA"}


def test_backtester_discovers_configurable_strategy() -> None:
    app = AppTest.from_file("../apps/backtester/app.py", default_timeout=15).run()
    app.selectbox(key="strategy_id").select("moving_average").run()

    assert not app.exception
    assert app.number_input(key="strategy_moving_average_fast_window").value == 20
    assert app.number_input(key="strategy_moving_average_slow_window").value == 60
