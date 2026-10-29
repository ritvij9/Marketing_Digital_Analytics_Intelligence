import pandas as pd
import pytest

from marketing_analytics.metrics import (
    build_session_funnel,
    validate_event_data,
)


def test_funnel_counts_sessions_not_repeated_events():
    events = pd.DataFrame(
        {
            "user_pseudo_id": ["u1", "u1", "u1", "u2", "u2"],
            "ga_session_id": [10, 10, 10, 20, 20],
            "event_name": [
                "page_view",
                "page_view",
                "add_to_cart",
                "page_view",
                "purchase",
            ],
        }
    )

    result = build_session_funnel(events).set_index("event_name")

    assert result.loc["page_view", "sessions"] == 2
    assert result.loc["add_to_cart", "sessions"] == 1
    assert result.loc["purchase", "sessions"] == 1


def test_funnel_excludes_events_without_complete_session_keys():
    events = pd.DataFrame(
        {
            "user_pseudo_id": ["u1", None],
            "ga_session_id": [10, 20],
            "event_name": ["page_view", "purchase"],
        }
    )

    result = build_session_funnel(events).set_index("event_name")

    assert result.loc["page_view", "sessions"] == 1
    assert result.loc["purchase", "sessions"] == 0


def test_validation_rejects_missing_columns():
    events = pd.DataFrame({"event_name": ["page_view"]})

    with pytest.raises(ValueError, match="Missing required columns"):
        validate_event_data(events)


def test_validation_rejects_empty_data():
    events = pd.DataFrame(
        columns=["user_pseudo_id", "ga_session_id", "event_name"]
    )

    with pytest.raises(ValueError, match="must not be empty"):
        validate_event_data(events)
