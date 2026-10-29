
import pandas as pd

from marketing_analytics.database import run_session_acquisition_distribution


def test_acquisition_distribution_counts_sessions(tmp_path) -> None:
    sql_path = (
        tmp_path / "session_acquisition_distribution.sql"
    )
    sql_path.write_text(
        """
        WITH session_sources AS (
            SELECT
                user_pseudo_id,
                ga_session_id,
                MIN(traffic_source) AS traffic_source,
                MIN(traffic_medium) AS traffic_medium,
                MIN(traffic_campaign) AS traffic_campaign
            FROM events
            WHERE user_pseudo_id IS NOT NULL
              AND ga_session_id IS NOT NULL
            GROUP BY user_pseudo_id, ga_session_id
        )
        SELECT
            traffic_source,
            traffic_medium,
            traffic_campaign,
            COUNT(*) AS sessions,
            ROUND(
                100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
                2
            ) AS session_percentage
        FROM session_sources
        GROUP BY 1, 2, 3
        ORDER BY sessions DESC
        """,
        encoding="utf-8",
    )

    events = pd.DataFrame(
        [
            ["u1", 101, "google", "organic", "(organic)"],
            ["u1", 101, "google", "organic", "(organic)"],
            ["u2", 202, "google", "organic", "(organic)"],
            ["u3", 303, "(direct)", "(none)", "(direct)"],
        ],
        columns=[
            "user_pseudo_id",
            "ga_session_id",
            "traffic_source",
            "traffic_medium",
            "traffic_campaign",
        ],
    )

    result = run_session_acquisition_distribution(
        events,
        sql_path=sql_path,
    )

    google = result[result["traffic_source"] == "google"].iloc[0]
    direct = result[result["traffic_source"] == "(direct)"].iloc[0]

    assert google["sessions"] == 2
    assert google["session_percentage"] == 66.67
    assert direct["sessions"] == 1
    assert direct["session_percentage"] == 33.33
    assert result["sessions"].sum() == 3
