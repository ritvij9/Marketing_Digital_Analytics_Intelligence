# Marketing & Digital Analytics Intelligence

A reproducible marketing analytics project that investigates ecommerce acquisition performance, session conversion, funnel-event coverage, and analytics data quality using the Google Analytics 4 (GA4) public ecommerce sample.

The goal is to turn raw event data into evidence-backed business findings while making analytical limitations explicit.

## Business Questions

- How many sessions and converting sessions occurred during the reporting period?
- How does observed session conversion vary across first-user traffic-source categories?
- How much uncertainty surrounds the observed conversion rates?
- How many sessions contain key ecommerce events?
- How consistent are acquisition parameters recorded within sessions?
- What can the available data support, and which marketing decisions require additional evidence?

## Project Scope

**Reporting period:** 1–7 January 2021  
**Data source:** GA4 public ecommerce sample  
**Analysis type:** Observational  
**Primary tools:** Python, pandas, DuckDB, SQL, Streamlit, pytest, Ruff

The project includes data ingestion, SQL-based analysis, acquisition diagnostics, conversion-rate confidence intervals, automated tests, documented findings, and an interactive dashboard.

## Key Findings

The current analysis reports:

- **26,331** distinct sessions
- **136** converting sessions
- **0.52%** overall session conversion rate

A converting session is a session containing at least one purchase event. This metric does not independently establish a unique completed order.

Acquisition categories show different observed conversion rates. However, these categories use first-user traffic-source fields rather than validated session-level attribution. Differences should not be interpreted as causal marketing impact.

Conversion-rate confidence intervals help communicate uncertainty, particularly for categories with small sample sizes.

The project also identifies sessions with conflicting event-parameter acquisition values. These conflicts warrant investigation but do not, on their own, prove a tracking defect.

See [`reports/findings_and_recommendations.md`](reports/findings_and_recommendations.md) for the business findings and [`reports/evidence_map.md`](reports/evidence_map.md) for links between findings and analytical evidence.

## Analytical Components

| Component | Purpose |
|---|---|
| Session funnel-event coverage | Counts sessions containing selected ecommerce events |
| Acquisition conversion analysis | Summarizes sessions and converting sessions by acquisition category |
| Acquisition distribution | Examines the distribution of acquisition dimensions |
| Acquisition conflict diagnostics | Identifies conflicting event-parameter acquisition values |
| Conversion uncertainty | Calculates Wilson confidence intervals and sample-size flags |
| Streamlit dashboard | Presents summary metrics, acquisition performance, event coverage, and data-quality diagnostics |

**Important:** Funnel-event counts measure event presence within sessions. They do not establish that users progressed through a validated sequential funnel.

## Repository Structure

```text
Marketing_Digital_Analytics_Intelligence/
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
├── reports/
│   ├── findings_and_recommendations.md
│   └── evidence_map.md
├── sql/
│   └── intermediate/
├── src/
│   └── marketing_analytics/
│       ├── dashboard.py
│       ├── ingestion.py
│       ├── database.py
│       ├── metrics.py
│       ├── conversion_statistics.py
│       └── run_*.py
├── tests/
├── pyproject.toml
├── requirements.txt
└── README.md
```

Raw and processed data files are excluded from Git. The data directories are preserved using `.gitkeep` files. You must obtain or generate the required input data before running the analyses.

## Setup

The project uses Python 3.14 or later.

From the repository root, create and activate a virtual environment in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

The project dependencies are declared in `requirements.txt` and `pyproject.toml`.

## Running the Analysis

Run commands from the repository root with the virtual environment activated.

The analysis runners are available as Python modules:

```powershell
python -m marketing_analytics.run_analysis
python -m marketing_analytics.run_acquisition_analysis
python -m marketing_analytics.run_acquisition_conflicts
python -m marketing_analytics.run_acquisition_distribution
python -m marketing_analytics.run_acquisition_conversion
python -m marketing_analytics.run_conversion_statistics
python -m marketing_analytics.run_traffic_source_analysis
```

These runners depend on the input files and paths expected by their implementations. Obtain the GA4 sample data and place the required files in the expected locations before executing them. Run the relevant upstream analyses before generating dependent outputs.

## Launching the Dashboard

After generating the required processed CSV files, launch the dashboard:

```powershell
python -m streamlit run src/marketing_analytics/dashboard.py
```

Open the local URL printed by Streamlit, usually `http://localhost:8501`.

The dashboard includes an executive overview, acquisition performance, conversion uncertainty, funnel-event coverage, acquisition data quality, and decision guardrails.

## Testing and Code Quality

Run the automated tests:

```powershell
python -m pytest
```

Run the code-quality checks:

```powershell
python -m ruff check .
```

The current test suite contains 22 tests, covering acquisition distribution, acquisition quality, conversion statistics, metrics, package configuration, and SQL funnel logic.

## Interpretation Guardrails

This project deliberately avoids unsupported business claims:

- **No ROAS or CAC claims:** marketing spend is unavailable.
- **No causal lift claims:** the analysis is observational, not a randomized experiment.
- **No automatic budget recommendations:** attribution and statistical uncertainty must be considered.
- **No unique-order assumptions:** purchase events and transaction identifiers require separate reconciliation.
- **No automatic tracking-defect conclusions:** conflicting acquisition values require investigation.

## Limitations and Future Improvements

- Validate session-level attribution before making channel-performance decisions.
- Reconcile purchase events and transaction identifiers before reporting unique completed orders.
- Validate event ordering before treating event counts as a sequential conversion funnel.
- Incorporate marketing spend and reliable attribution data before estimating ROAS or CAC.
- Add a fully documented data acquisition and clean-checkout reproduction workflow.

## Project Status

The repository includes the analytical scripts, SQL transformations, generated analytical outputs from the local workflow, evidence-backed findings, an interactive dashboard, and an automated test suite.

The project is designed to demonstrate reproducible analysis, statistical caution, data-quality investigation, and business-oriented interpretation—not merely the production of charts.
