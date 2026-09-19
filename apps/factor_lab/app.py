"""UI skeleton for the cross-sectional factor-research milestone."""

import streamlit as st

st.set_page_config(page_title="Factor Research Lab", page_icon="🧪", layout="wide")
st.title("Cross-sectional factor research lab")
st.caption("Milestone 2 · application skeleton")

st.warning("The research pipeline is not implemented yet; this page defines its public contract.")

universe = st.multiselect(
    "Research universe",
    ["US sector ETFs", "Large-cap equities", "User-uploaded prices"],
    default=["US sector ETFs"],
)
factor = st.selectbox("Factor", ["12–1 momentum", "Low volatility", "Trend strength"])
rebalance = st.selectbox("Rebalance frequency", ["Monthly", "Weekly", "Quarterly"])

st.subheader("Planned outputs")
st.markdown(
    """
- Data-quality and universe-coverage report
- Factor ranks, quantile returns, information coefficient, and turnover
- Equal-weight and volatility-scaled long/short portfolios
- Transaction-cost sensitivity and walk-forward validation
- Benchmark-relative tear sheet with downloadable experiment metadata
"""
)
st.write(
    "Selected research specification:",
    {"universe": universe, "factor": factor, "rebalance": rebalance},
)
