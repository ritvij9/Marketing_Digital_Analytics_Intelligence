# Evidence Map — Marketing & Digital Analytics Intelligence

## Purpose

This document links the business findings in `findings_and_recommendations.md` to the analytical scripts, generated outputs, and validation evidence supporting them.

The analysis uses the GA4 public ecommerce sample for 1–7 January 2021. Generated CSVs are reproducible outputs and may be excluded from Git; the scripts and SQL models are the version-controlled implementation.

## Findings-to-Evidence Mapping

| Business finding | Analytical implementation | Expected output | Interpretation and limitations |
|---|---|---|---|
| Overall session conversion rate is approximately 0.52% | `run_acquisition_conversion.py` | `data/processed/session_acquisition_conversion_20210101_20210107.csv` | Based on 136 converting sessions out of 26,331 session keys. A purchase event is not independently verified as a unique completed order. |
| Funnel-event coverage differs by event | `run_analysis.py` and `session_funnel.sql` | `data/processed/session_funnel_20210101_20210107.csv` | Counts distinct sessions containing each event. Does not establish sequential stage progression. |
| Acquisition metadata coverage and conflicts require investigation | `run_acquisition_analysis.py`, `run_acquisition_conflicts.py` | `acquisition_quality_20210101_20210107.csv` and `acquisition_conflict_details_20210101_20210107.csv` | Uses event-parameter acquisition fields. Multiple values within a session do not, by themselves, prove tracking is defective. |
| First-user acquisition categories have different observed conversion rates | `run_acquisition_conversion.py` and `session_acquisition_conversion.sql` | `session_acquisition_conversion_20210101_20210107.csv` | The available `traffic_source` fields represent first-user acquisition, not validated session-level attribution. |
| Conversion rates have substantial uncertainty, particularly for small groups | `run_conversion_statistics.py` and `conversion_statistics.py` | `acquisition_conversion_uncertainty_20210101_20210107.csv` | Uses 95% Wilson confidence intervals. The 200-session threshold is a screening heuristic, not a statistical significance test. |
| Purchase and revenue metrics need transaction-level reconciliation | Source-level BigQuery validation | Validation query/results to be documented separately | Earlier validation found 144 purchase events, 138 with an event-parameter transaction ID, and 136 distinct event-parameter transaction IDs. Revenue sums were USD 7,982. The complete validation procedure is not yet packaged as a reproducible repository deliverable. |
| ROAS, CAC, and marketing budget efficiency cannot currently be calculated | Dataset feasibility and field-availability assessment | No supported cost-efficiency output | Marketing spend is unavailable at a suitable grain. Do not infer profitability or incremental marketing impact from conversion rates alone. |

## Reproducibility

Run commands from the repository root with the project virtual environment activated.

```powershell
python -m marketing_analytics.run_analysis
python -m marketing_analytics.run_acquisition_analysis
python -m marketing_analytics.run_acquisition_conflicts
python -m marketing_analytics.run_traffic_source_analysis
python -m marketing_analytics.run_acquisition_distribution
python -m marketing_analytics.run_acquisition_conversion
python -m marketing_analytics.run_conversion_statistics
```

The required raw GA4 extracts must exist in `data/raw/`. The statistical analysis requires the acquisition conversion output to have been generated first.

## Evidence Quality Rules

1. Distinguish event counts, session counts, converting sessions, and unique orders.
2. Preserve the grain and definition of every metric.
3. Do not describe event-presence counts as a sequential funnel.
4. Do not describe first-user traffic source as validated session attribution.
5. Treat confidence intervals as uncertainty estimates, not automatic proof of significant differences.
6. Do not make ROAS, CAC, causal-lift, or budget-allocation claims without the required data and methodology.
7. Treat generated outputs as reproducible artifacts, not as independently validated evidence merely because a file exists.

## Current Status

The principal analysis scripts, SQL models, conversion uncertainty utility, tests, and business findings report have been implemented. The mapping above documents their intended relationships; it does not replace independent reconciliation of the outputs.

The next reporting-layer milestone is to build a dashboard whose displayed KPIs reconcile with these analytical outputs and whose limitations remain visible.