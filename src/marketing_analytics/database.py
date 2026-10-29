
"""DuckDB execution utilities for marketing analytics."""

from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd

REQUIRED_EVENT_COLUMNS = {
    "user_pseudo_id",
    "ga_session_id",
    "event_name",
}

REQUIRED_ACQUISITION_COLUMNS = {
    "user_pseudo_id",
    "ga_session_id",
    "event_source",
    "event_medium",
    "event_campaign",
}


def _run_sql_model(
    events: pd.DataFrame,
    sql_path: Path,
    required_columns: set[str],
) -> pd.DataFrame:
    """Validate event data and execute a DuckDB SQL model."""
    missing_columns = required_columns - set(events.columns)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))

        if required_columns == REQUIRED_EVENT_COLUMNS:
            raise ValueError(
                f"Missing required event columns: {missing}"
            )

        raise ValueError(f"Missing required columns: {missing}")

    if events.empty:
        raise ValueError("Event data must not be empty.")

    if not sql_path.is_file():
        raise FileNotFoundError(f"SQL model not found: {sql_path}")

    connection = duckdb.connect(":memory:")

    try:
        connection.register("events", events)
        sql = sql_path.read_text(encoding="utf-8-sig")
        return connection.execute(sql).df()
    finally:
        connection.close()


def run_session_funnel(
    events: pd.DataFrame,
    sql_path: Path | None = None,
) -> pd.DataFrame:
    """Run the session funnel using event-presence counts."""
    if sql_path is None:
        sql_path = (
            Path(__file__).resolve().parents[2]
            / "sql"
            / "intermediate"
            / "session_funnel.sql"
        )

    return _run_sql_model(
        events=events,
        sql_path=sql_path,
        required_columns=REQUIRED_EVENT_COLUMNS,
    )


def run_session_acquisition_quality(
    events: pd.DataFrame,
    sql_path: Path | None = None,
) -> pd.DataFrame:
    """Measure session-level acquisition coverage and conflicts."""
    if sql_path is None:
        sql_path = (
            Path(__file__).resolve().parents[2]
            / "sql"
            / "intermediate"
            / "session_acquisition_quality.sql"
        )

    return _run_sql_model(
        events=events,
        sql_path=sql_path,
        required_columns=REQUIRED_ACQUISITION_COLUMNS,
    )


def run_acquisition_conflict_details(
    events: pd.DataFrame,
    sql_path: Path | None = None,
) -> pd.DataFrame:
    """Return session-level details for conflicting acquisition metadata."""
    if sql_path is None:
        sql_path = (
            Path(__file__).resolve().parents[2]
            / "sql"
            / "intermediate"
            / "acquisition_conflict_details.sql"
        )

    return _run_sql_model(
        events=events,
        sql_path=sql_path,
        required_columns=REQUIRED_ACQUISITION_COLUMNS,
    )


def run_session_traffic_source(
    events: pd.DataFrame,
    sql_path: Path | None = None,
) -> pd.DataFrame:
    """Summarize traffic-source consistency across sessions."""
    if sql_path is None:
        sql_path = (
            Path(__file__).resolve().parents[2]
            / "sql"
            / "intermediate"
            / "session_traffic_source.sql"
        )

    required_columns = {
        "user_pseudo_id",
        "ga_session_id",
        "traffic_source",
        "traffic_medium",
        "traffic_campaign",
    }

    return _run_sql_model(
        events=events,
        sql_path=sql_path,
        required_columns=required_columns,
    )


def run_session_acquisition_distribution(
    events: pd.DataFrame,
    sql_path: Path | None = None,
) -> pd.DataFrame:
    """Summarize sessions by traffic-source, medium, and campaign."""
    if sql_path is None:
        sql_path = (
            Path(__file__).resolve().parents[2]
            / "sql"
            / "intermediate"
            / "session_acquisition_distribution.sql"
        )

    required_columns = {
        "user_pseudo_id",
        "ga_session_id",
        "traffic_source",
        "traffic_medium",
        "traffic_campaign",
    }

    return _run_sql_model(
        events=events,
        sql_path=sql_path,
        required_columns=required_columns,
    )


def run_session_acquisition_conversion(
    events: pd.DataFrame,
    sql_path: Path | None = None,
) -> pd.DataFrame:
    """Calculate purchase conversion rates by acquisition combination."""
    if sql_path is None:
        sql_path = (
            Path(__file__).resolve().parents[2]
            / "sql"
            / "intermediate"
            / "session_acquisition_conversion.sql"
        )

    required_columns = {
        "user_pseudo_id",
        "ga_session_id",
        "event_name",
        "traffic_source",
        "traffic_medium",
        "traffic_campaign",
    }

    return _run_sql_model(
        events=events,
        sql_path=sql_path,
        required_columns=required_columns,
    )
