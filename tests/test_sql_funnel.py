from pathlib import Path

import pandas as pd
import pytest

from marketing_analytics.database import run_session_funnel


def test_sql_funnel_matches_expected_session_counts():
    events = pd.DataFrame(
        {
            "user_pseudo_id": ["u1", "u1", "u1", "u2", "u2", "u3", None],
            "ga_session_id": [10, 10, 10, 20, 20, 30, 40],
            "event_name": [
                "page_view",
                "page_view",
                "add_to_cart",
                "page_view",
                "purchase",
                "view_item",
                "purchase",
            ],
        }
    )

    result = run_session_funnel(events)
    actual = result.set_index("event_name")["sessions"].to_dict()

    assert actual == {
        "page_view": 2,
        "view_item": 1,
        "add_to_cart": 1,
        "begin_checkout": 0,
        "add_shipping_info": 0,
        "add_payment_info": 0,
        "purchase": 1,
    }


def test_sql_funnel_rejects_missing_sql_model(tmp_path: Path):
    events = pd.DataFrame(
        {
            "user_pseudo_id": ["u1"],
            "ga_session_id": [10],
            "event_name": ["page_view"],
        }
    )

    with pytest.raises(FileNotFoundError, match="SQL model not found"):
        run_session_funnel(events, tmp_path / "missing.sql")

def test_sql_funnel_rejects_missing_event_columns():
    events = pd.DataFrame({"event_name": ["page_view"]})

    with pytest.raises(
        ValueError,
        match="Missing required event columns",
    ):
        run_session_funnel(events)


def test_sql_funnel_rejects_empty_event_data():
    events = pd.DataFrame(
        columns=["user_pseudo_id", "ga_session_id", "event_name"]
    )

    with pytest.raises(ValueError, match="must not be empty"):
        run_session_funnel(events)
