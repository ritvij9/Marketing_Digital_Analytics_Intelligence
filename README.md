
# Marketing & Digital Analytics Intelligence

A reproducible marketing analytics project investigating ecommerce acquisition performance, session conversion, funnel-event coverage, and acquisition data quality using the Google Analytics 4 (GA4) public ecommerce sample.

The project combines SQL-based analysis, Python data processing, statistical uncertainty estimation, automated testing, and an interactive Streamlit dashboard to turn event-level data into evidence-backed business findings.

## Overview

**Reporting period:** 1–7 January 2021  
**Data source:** GA4 public ecommerce sample  
**Analysis type:** Observational  
**Primary tools:** Python, pandas, DuckDB, SQL, Streamlit, pytest, Ruff

### Business questions

- How many sessions and converting sessions occurred during the reporting period?
- How does observed session conversion vary across first-user traffic-source categories?
- How much uncertainty surrounds the observed conversion rates?
- How many sessions contain key ecommerce events?
- How consistent are acquisition parameters recorded within sessions?
- What conclusions can the available data support, and where is additional evidence needed?

## Key Findings

The current analysis reports:

| Metric | Result |
|---|---:|
| Distinct sessions | 26,331 |
| Converting sessions | 136 |
| Overall session conversion rate | 0.52% |

A converting session is a session containing at least one purchase event. It does not independently establish a unique completed order.

The analysis also finds variation in observed conversion rates across acquisition categories. These categories use GA4 first-user traffic-source fields rather than validated session-level attribution. Differences should therefore be treated as descriptive, not as evidence of causal marketing impact.

Wilson confidence intervals communicate uncertainty around conversion rates, particularly for categories with small sample sizes. Acquisition quality diagnostics identify sessions with conflicting event-parameter acquisition values. Such conflicts warrant investigation but do not, on their own, prove a tracking defect.

For detailed findings and recommendations, see [`reports/findings_and_recommendations.md`](reports/findings_and_recommendations.md). For traceability between findings and analytical outputs, see [`reports/evidence_map.md`](reports/evidence_map.md).

## Dashboard

The Streamlit dashboard presents:

- Executive summary metrics
- Observed session conversion rates by acquisition category
- Acquisition detail, including confidence intervals and sample-size flags where available
- Sessions containing selected funnel events
- Acquisition data-quality diagnostics
- Guardrails against unsupported marketing conclusions

The dashboard reads generated CSV reports from `data/processed/`; it does not recompute the analyses itself.

### Launch the dashboard

After installing dependencies and generating the required reports:

```powershell
python -m streamlit run src/marketing_analytics/dashboard.py
```

Open the local URL printed by Streamlit, usually `http://localhost:8501`.

## Analytical Components

| Component | Purpose |
|---|---|
| Session funnel-event coverage | Counts sessions containing selected ecommerce events |
| Acquisition quality analysis | Measures acquisition-data coverage and conflicts |
| Acquisition conflict details | Identifies sessions with conflicting acquisition metadata |
| Acquisition distribution | Summarizes sessions by traffic source, medium, and campaign |
| Traffic-source consistency | Examines consistency of first-user traffic-source values across sessions |
| Acquisition conversion | Calculates converting sessions and observed conversion rates by acquisition category |
| Conversion uncertainty | Calculates Wilson confidence intervals and sample-size flags |
| Interactive dashboard | Presents the generated analytical outputs for review |

## Repository Structure

```text
Marketing_Digital_Analytics_Intelligence/
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
├── reports/
│   ├── findings_and_recommendations.md
│   ├── evidence_map.md
│   └── figures/
├── sql/
│   └── intermediate/
├── src/
│   └── marketing_analytics/
│       ├── ingestion.py
│       ├── database.py
│       ├── metrics.py
│       ├── conversion_statistics.py
│       ├── dashboard.py
│       └── run_*.py
├── tests/
├── pyproject.toml
├── requirements.txt
└── README.md
```

Raw data, processed CSV reports, local databases, virtual environments, and generated package metadata are excluded from Git. The data directories are retained using `.gitkeep` files.

## Setup

The project requires Python 3.14 or later, as specified in `pyproject.toml`.

From the repository root, create and activate a virtual environment in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

Dependencies are declared in `requirements.txt` and referenced by the project configuration.

## Data Requirements

The analysis uses three local CSV extracts for 1–7 January 2021. Place them in `data/raw/` using these exact filenames:

| Input file | Used for |
|---|---|
| `ga4_events_20210101_20210107.csv` | Session funnel-event analysis |
| `ga4_events_acquisition_20210101_20210107.csv` | Acquisition coverage and conflict diagnostics |
| `ga4_events_traffic_source_20210101_20210107.csv` | Acquisition distribution, consistency, and conversion analysis |

The files are not included in the Git repository. Obtain or generate the corresponding extracts from the GA4 public ecommerce sample before running the analyses.

The local ingestion code validates required columns and rejects missing or empty input files. Each extract must contain the columns expected by its corresponding analysis.

**Reproducibility note:** the analysis runners consume local CSV files; they do not automatically download the source data. A fresh clone requires data preparation before the analytical pipeline and dashboard can run.

## Running the Analysis

Run the following commands from the repository root with the virtual environment activated.

### 1. Session funnel-event coverage

```powershell
python -m marketing_analytics.run_analysis
```

Reads `ga4_events_20210101_20210107.csv` and writes:

`data/processed/session_funnel_20210101_20210107.csv`

### 2. Acquisition data quality

```powershell
python -m marketing_analytics.run_acquisition_analysis
```

Reads `ga4_events_acquisition_20210101_20210107.csv` and writes:

`data/processed/acquisition_quality_20210101_20210107.csv`

### 3. Acquisition conflict details

```powershell
python -m marketing_analytics.run_acquisition_conflicts
```

Uses the event-parameter acquisition extract and writes:

`data/processed/acquisition_conflict_details_20210101_20210107.csv`

### 4. Acquisition distribution

```powershell
python -m marketing_analytics.run_acquisition_distribution
```

Reads `ga4_events_traffic_source_20210101_20210107.csv` and writes:

`data/processed/session_acquisition_distribution_20210101_20210107.csv`

### 5. Traffic-source consistency

```powershell
python -m marketing_analytics.run_traffic_source_analysis
```

Uses the traffic-source extract and writes:

`data/processed/traffic_source_session_quality_20210101_20210107.csv`

### 6. Acquisition conversion analysis

```powershell
python -m marketing_analytics.run_acquisition_conversion
```

Uses the traffic-source extract and writes:

`data/processed/session_acquisition_conversion_20210101_20210107.csv`

### 7. Conversion uncertainty

Run this after the acquisition conversion analysis:

```powershell
python -m marketing_analytics.run_conversion_statistics
```

Reads the acquisition conversion report and writes:

`data/processed/acquisition_conversion_uncertainty_20210101_20210107.csv`

This report includes Wilson confidence intervals and sample-size status flags.

## Testing and Code Quality

Run the automated test suite:

```powershell
python -m pytest
```

Run Ruff code-quality checks:

```powershell
python -m ruff check .
```

The current test suite contains 22 tests covering acquisition distribution, acquisition quality, conversion statistics, metrics, package configuration, and SQL funnel logic.

## Interpretation Guardrails

The project deliberately avoids unsupported business conclusions.

- **No ROAS or CAC claims:** marketing spend is unavailable.
- **No causal lift claims:** the analysis is observational, not a randomized experiment.
- **No automatic budget recommendations:** attribution and statistical uncertainty need to be considered.
- **No unique-order assumptions:** purchase events and transaction identifiers require separate reconciliation.
- **No automatic tracking-defect conclusions:** conflicting acquisition values warrant investigation but do not prove a tracking defect.

### Important analytical limitations

**Attribution:** Acquisition categories use first-user traffic-source fields, not validated session-level attribution.

**Funnel interpretation:** Event counts represent sessions containing an event. They do not establish that sessions progressed through a validated sequence of funnel stages.

**Statistical uncertainty:** Confidence intervals describe uncertainty around individual rates. They are not, by themselves, formal tests of differences between acquisition categories. Small groups can produce unstable rates.

**Business economics:** Without marketing spend and reliable attribution, the project cannot establish ROAS, CAC, incremental lift, or an optimal budget allocation.

**Transaction validation:** Purchase-event counts and transaction identifiers require reconciliation before they can support unique-order reporting.

## Future Improvements

Potential extensions include:

- Documented, repeatable extraction of the required GA4 sample data
- Stronger session-level attribution validation
- Explicit sequential funnel validation
- Purchase-event and transaction-ID reconciliation
- Integration of marketing spend for ROAS and CAC analysis
- Expanded tests for data contracts and end-to-end pipeline execution

## Project Status

The repository contains SQL analytical models, Python execution modules, conversion uncertainty analysis, data-quality diagnostics, an interactive dashboard, evidence-backed reports, and an automated test suite.

The focus is on reproducible analytical work, sound interpretation, data-quality investigation, and business relevance—not just chart generation.
