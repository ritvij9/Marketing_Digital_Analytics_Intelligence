"""Validated metric calculations for marketing analytics."""

from __future__ import annotations

import pandas as pd

REQUIRED_SESSION_COLUMNS = {
    "user_pseudo_id",
    "ga_session_id",
    "event_name",
}


def validate_event_data(events: pd.DataFrame) -> None:
    """Validate the minimum schema required for session-level analysis."""
    missing_columns = REQUIRED_SESSION_COLUMNS - set(events.columns)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")

    if events.empty:
        raise ValueError("Event data must not be empty.")


def build_session_funnel(events: pd.DataFrame) -> pd.DataFrame:
    """Count distinct user-session keys containing each funnel event.

    This measures session-level event presence, not sequential conversion.
    """
    validate_event_data(events)

    valid_events = events.loc[
        events["user_pseudo_id"].notna()
        & events["ga_session_id"].notna()
    ].copy()

    valid_events["session_key"] = list(
        zip(
            valid_events["user_pseudo_id"],
            valid_events["ga_session_id"],
            strict=True,
        )
    )

    funnel_events = [
        "page_view",
        "view_item",
        "add_to_cart",
        "begin_checkout",
        "add_shipping_info",
        "add_payment_info",
        "purchase",
    ]

    rows = []

    for event_name in funnel_events:
        session_count = valid_events.loc[
            valid_events["event_name"].eq(event_name),
            "session_key",
        ].nunique()

        rows.append(
            {
                "event_name": event_name,
                "sessions": session_count,
            }
        )

    return pd.DataFrame(rows)
