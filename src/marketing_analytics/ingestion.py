"""Load and validate the local GA4 event extract."""

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = {
    "user_pseudo_id",
    "ga_session_id",
    "event_name",
    "event_date",
    "event_timestamp",
}


def load_ga4_events(path: Path) -> pd.DataFrame:
    """Load GA4 events while preserving identifiers as strings."""
    if not path.is_file():
        raise FileNotFoundError(f"GA4 extract not found: {path}")

    events = pd.read_csv(
        path,
        dtype={
            "user_pseudo_id": "string",
            "ga_session_id": "Int64",
            "event_name": "string",
            "event_date": "Int64",
            "event_timestamp": "Int64",
        },
    )

    missing_columns = REQUIRED_COLUMNS - set(events.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required GA4 columns: {missing}")

    if events.empty:
        raise ValueError("GA4 extract must not be empty.")

    return events
