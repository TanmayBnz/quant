# Roadmap

## Milestone 1 — trustworthy single-asset backtester

- [x] Source-layout Python package
- [x] Deterministic offline data
- [x] Strategy protocol and moving-average baseline
- [x] One-period signal delay
- [x] Commission and slippage model
- [x] Benchmark, drawdown, and core risk metrics
- [x] Automated tests and CI definition
- [x] Backtester dashboard and deployment container
- [x] Automatic discovery of strategies outside the engine package
- [x] Strategy parameter metadata and generated dashboard controls
- [x] Multi-ticker batch comparison with isolated failures
- [x] Optional Yahoo Finance adjusted-close adapter
- [x] Interview-review notes in `learning/`
- [ ] Trade ledger aligned with the engine's execution convention
- [ ] CSV upload
- [ ] Parameter sweep with an explicit out-of-sample split
- [ ] Exportable experiment configuration and results

## Milestone 2 — cross-sectional factor lab

- [ ] Multi-asset price schema and data-quality report
- [ ] Point-in-time universe policy
- [ ] Momentum, low-volatility, and trend factors
- [ ] Cross-sectional ranks, quantiles, and information coefficient
- [ ] Rebalance calendar and portfolio weights
- [ ] Volatility scaling, caps, and transaction costs
- [ ] Walk-forward validation and benchmark-relative tear sheet
- [ ] Cached data refresh and deployed application

## Milestone 3 — paper portfolio and risk monitor

- [ ] Persistent portfolio, order, fill, and job-run models
- [ ] Idempotent daily signal and rebalance job
- [ ] Simulated fill rules and reconciliation
- [ ] Exposure, P&L attribution, volatility, and drawdown views
- [ ] Data freshness and pipeline-health checks
- [ ] Alerts for failures and risk-limit breaches
- [ ] Backtest-versus-paper tracking
- [ ] Scheduled deployment with an educational-use disclaimer

## Portfolio polish

- [ ] Public demo links and screenshots
- [ ] Short research report for each application
- [ ] Architecture and methodology diagrams
- [ ] Reproducible sample datasets with provenance
- [ ] Release tags and concise resume bullets
