
import pandas as pd
import pytest

from marketing_analytics.database import run_session_acquisition_quality


@pytest.fixture
def acquisition_events() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "user_pseudo_id": "user_1",
                "ga_session_id": 101,
                "event_source": "google",
                "event_medium": "organic",
                "event_campaign": None,
            },
            {
                "user_pseudo_id": "user_1",
                "ga_session_id": 101,
                "event_source": "google",
                "event_medium": "organic",
                "event_campaign": None,
            },
            {
                "user_pseudo_id": "user_2",
                "ga_session_id": 202,
                "event_source": "google",
                "event_medium": "cpc",
                "event_campaign": "spring_sale",
            },
            {
                "user_pseudo_id": "user_2",
                "ga_session_id": 202,
                "event_source": "bing",
                "event_medium": "cpc",
                "event_campaign": "spring_sale",
            },
            {
                "user_pseudo_id": "user_3",
                "ga_session_id": 303,
                "event_source": None,
                "event_medium": None,
                "event_campaign": None,
            },
        ]
    )


def test_acquisition_quality_counts_sessions_and_conflicts(
    acquisition_events: pd.DataFrame,
) -> None:
    result = run_session_acquisition_quality(acquisition_events)
    row = result.iloc[0]

    assert row["total_sessions"] == 3
    assert row["sessions_with_source"] == 2
    assert row["sessions_with_medium"] == 2
    assert row["sessions_with_campaign"] == 1
    assert row["sessions_with_any_acquisition_data"] == 2
    assert row["sessions_with_source_conflicts"] == 1
    assert row["sessions_with_medium_conflicts"] == 0
    assert row["sessions_with_campaign_conflicts"] == 0
    assert row["sessions_with_any_acquisition_conflict"] == 1


def test_acquisition_quality_rejects_missing_columns() -> None:
    events = pd.DataFrame(
        {
            "user_pseudo_id": ["user_1"],
            "ga_session_id": [101],
        }
    )

    with pytest.raises(ValueError, match="Missing required columns"):
        run_session_acquisition_quality(events)


def test_acquisition_quality_rejects_empty_data() -> None:
    events = pd.DataFrame(
        columns=[
            "user_pseudo_id",
            "ga_session_id",
            "event_source",
            "event_medium",
            "event_campaign",
        ]
    )

    with pytest.raises(ValueError, match="must not be empty"):
        run_session_acquisition_quality(events)
