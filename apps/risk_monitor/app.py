"""UI skeleton for the scheduled paper portfolio and risk monitor."""

from datetime import UTC, datetime

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Paper Portfolio Monitor", page_icon="🛡️", layout="wide")
st.title("Paper-trading and risk monitor")
st.caption("Milestone 3 · application skeleton")

st.warning("No broker is connected. All future orders and fills in this project are simulated.")

status = st.columns(4)
status[0].metric("Pipeline", "Not configured")
status[1].metric("Positions", "0")
status[2].metric("Gross exposure", "0.0%")
status[3].metric("Drawdown", "0.0%")

st.subheader("Operational checks")
checks = pd.DataFrame(
    [
        {"check": "Market data freshness", "status": "pending"},
        {"check": "Signal job", "status": "pending"},
        {"check": "Duplicate-order guard", "status": "pending"},
        {"check": "Position reconciliation", "status": "pending"},
    ]
)
st.dataframe(checks, hide_index=True, width="stretch")
st.caption(f"Dashboard rendered {datetime.now(UTC).isoformat(timespec='seconds')}")
