
"""Decision-oriented marketing analytics dashboard."""

from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

FILES = {
    "funnel": "session_funnel_20210101_20210107.csv",
    "acquisition": "session_acquisition_conversion_20210101_20210107.csv",
    "uncertainty": "acquisition_conversion_uncertainty_20210101_20210107.csv",
    "quality": "acquisition_quality_20210101_20210107.csv",
}

st.set_page_config(
    page_title="Marketing Analytics Intelligence",
    page_icon="📊",
    layout="wide",
)


@st.cache_data
def load_csv(filename: str) -> pd.DataFrame | None:
    """Load a processed CSV, returning None if unavailable."""
    path = PROCESSED_DIR / filename

    if not path.is_file():
        return None

    return pd.read_csv(path)


def show_missing_file(filename: str, command: str) -> None:
    """Explain how to generate a missing analytical output."""
    st.warning(
        f"Required output is missing: `{filename}`. "
        "Run the corresponding command from the project root:"
    )
    st.code(command, language="powershell")


def format_integer(value: int | float) -> str:
    """Format a count for display."""
    return f"{value:,.0f}"


st.title("Marketing & Digital Analytics Intelligence")
st.caption(
    "GA4 public ecommerce sample | "
    "1–7 January 2021 | Observational analysis"
)

st.info(
    "Attribution caveat: acquisition categories use first-user traffic-source "
    "fields, not validated session-level attribution. Observed differences "
    "do not establish causal marketing impact."
)

# Load existing analytical outputs; do not recompute analyses here.
funnel = load_csv(FILES["funnel"])
acquisition = load_csv(FILES["acquisition"])
uncertainty = load_csv(FILES["uncertainty"])
quality = load_csv(FILES["quality"])

# Executive overview
st.header("Executive overview")

if acquisition is None:
    show_missing_file(
        FILES["acquisition"],
        "python -m marketing_analytics.run_acquisition_conversion",
    )
else:
    required = {"sessions", "converting_sessions"}
    missing = required - set(acquisition.columns)

    if missing:
        st.error(
            "The acquisition output is missing required columns: "
            + ", ".join(sorted(missing))
        )
    else:
        total_sessions = acquisition["sessions"].sum()
        converting_sessions = acquisition["converting_sessions"].sum()
        conversion_rate = (
            converting_sessions / total_sessions * 100
            if total_sessions
            else 0.0
        )

        col1, col2, col3 = st.columns(3)
        col1.metric("Sessions", format_integer(total_sessions))
        col2.metric(
            "Converting sessions",
            format_integer(converting_sessions),
        )
        col3.metric("Session conversion rate", f"{conversion_rate:.2f}%")

        st.caption(
            "A converting session contains at least one purchase event. "
            "This does not independently establish a unique completed order."
        )

st.divider()

# Acquisition performance
st.header("Acquisition performance")

if acquisition is None:
    show_missing_file(
        FILES["acquisition"],
        "python -m marketing_analytics.run_acquisition_conversion",
    )
else:
    display = acquisition.copy()

    dimension_columns = [
        column
        for column in [
            "traffic_source",
            "traffic_medium",
            "traffic_campaign",
        ]
        if column in display.columns
    ]

    required_columns = {"sessions", "converting_sessions"}

    if not dimension_columns:
        st.error("No acquisition dimension columns were found.")
    elif not required_columns.issubset(display.columns):
        st.error(
            "The acquisition output is missing required columns: "
            + ", ".join(sorted(required_columns - set(display.columns)))
        )
    else:
        display["acquisition_category"] = (
            display[dimension_columns]
            .fillna("(missing)")
            .astype(str)
            .agg(" / ".join, axis=1)
        )

        display["conversion_rate_pct"] = (
            display["converting_sessions"].div(
                display["sessions"].where(display["sessions"] > 0)
            )
            * 100
        )

        # Add confidence intervals when the expected columns are available.
        if uncertainty is not None:
            join_columns = [
                column
                for column in dimension_columns
                if column in uncertainty.columns
            ]
            interval_columns = [
                "ci_lower_pct",
                "ci_upper_pct",
                "sample_size_status",
            ]
            required_interval_columns = set(
                join_columns + interval_columns
            )

            if (
                join_columns
                and required_interval_columns.issubset(
                    uncertainty.columns
                )
            ):
                display = display.merge(
                    uncertainty[join_columns + interval_columns],
                    on=join_columns,
                    how="left",
                    validate="one_to_one",
                )

        st.subheader("Observed session conversion rate")
        st.caption(
            "Horizontal bars improve label readability. Check sample sizes "
            "and confidence intervals before interpreting rate differences."
        )

        chart_data = display[
            [
                "acquisition_category",
                "conversion_rate_pct",
                "sessions",
            ]
        ].copy()

        chart_data["chart_label"] = chart_data.apply(
            lambda row: (
                f"{row['acquisition_category'][:55]} "
                f"(n={row['sessions']:,.0f})"
            ),
            axis=1,
        )

        chart_data = chart_data.sort_values(
            "conversion_rate_pct",
            ascending=True,
        )

        st.bar_chart(
            chart_data.set_index("chart_label")["conversion_rate_pct"],
            horizontal=True,
            x_label="Session conversion rate (%)",
            y_label="Acquisition category and session count",
        )

        preferred_columns = [
            "acquisition_category",
            "sessions",
            "converting_sessions",
            "conversion_rate_pct",
            "ci_lower_pct",
            "ci_upper_pct",
            "sample_size_status",
        ]
        visible_columns = [
            column
            for column in preferred_columns
            if column in display.columns
        ]

        table = display[visible_columns].copy()

        if "conversion_rate_pct" in table.columns:
            table["conversion_rate_pct"] = table[
                "conversion_rate_pct"
            ].round(3)

        for column in ["ci_lower_pct", "ci_upper_pct"]:
            if column in table.columns:
                table[column] = table[column].round(3)

        st.subheader("Acquisition detail")
        st.dataframe(
            table,
            width="stretch",
            hide_index=True,
        )

        st.caption(
            "Confidence intervals describe uncertainty in individual rates; "
            "they are not formal tests of differences between categories. "
            "Small groups can produce highly unstable rates."
        )

        if uncertainty is None:
            show_missing_file(
                FILES["uncertainty"],
                "python -m marketing_analytics.run_conversion_statistics",
            )

st.divider()

# Funnel-event coverage
st.header("Funnel-event coverage")

if funnel is None:
    show_missing_file(
        FILES["funnel"],
        "python -m marketing_analytics.run_analysis",
    )
elif "event_name" not in funnel.columns:
    st.error("The funnel output does not contain an event_name column.")
else:
    st.subheader("Sessions containing each event")

    if "sessions" in funnel.columns:
        event_chart = funnel[["event_name", "sessions"]].copy()
        event_chart["sessions"] = pd.to_numeric(
            event_chart["sessions"],
            errors="coerce",
        )
        event_chart = event_chart.dropna(subset=["sessions"])
        event_chart = event_chart.sort_values(
            "sessions",
            ascending=True,
        )

        st.bar_chart(
            event_chart.set_index("event_name")["sessions"],
            horizontal=True,
            x_label="Sessions containing event",
            y_label="Event",
        )

    with st.expander("View funnel-event data"):
        st.dataframe(
            funnel,
            width="stretch",
            hide_index=True,
        )

    st.warning(
        "These are event-presence counts, not a validated sequential funnel. "
        "They do not prove that sessions progressed through the displayed "
        "events in order."
    )

st.divider()

# Acquisition data quality
st.header("Acquisition data quality")

if quality is None:
    show_missing_file(
        FILES["quality"],
        "python -m marketing_analytics.run_acquisition_analysis",
    )
else:
    st.dataframe(
        quality,
        width="stretch",
        hide_index=True,
    )

    st.caption(
        "This diagnostic uses event-parameter acquisition fields. Multiple "
        "distinct values within a session require investigation but do not, "
        "by themselves, prove a tracking defect."
    )

st.divider()

# Decision guardrails
st.header("Decision guardrails")

st.markdown(
    """
    - **No ROAS or CAC claims:** marketing spend is unavailable.
    - **No causal lift claims:** this is observational data, not a
      randomized experiment.
    - **No automatic budget recommendations:** attribution and uncertainty
      need to be considered.
    - **No unique-order assumptions:** purchase events and transaction
      identifiers require separate reconciliation.
    """
)

st.caption(
    "Source: GA4 public ecommerce sample. "
    "Reporting window: 1–7 January 2021."
)
