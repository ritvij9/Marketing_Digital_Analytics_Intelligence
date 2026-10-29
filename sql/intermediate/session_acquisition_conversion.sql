
-- Session conversion by GA4 traffic-source combination.
-- A converting session contains at least one purchase event.
-- Attribution fields come from the structured traffic_source export.
-- Session attribution uses MIN() as a provisional assignment rule.

WITH event_data AS (
    SELECT
        user_pseudo_id,
        ga_session_id,
        event_name,
        NULLIF(TRIM(traffic_source), '') AS traffic_source,
        NULLIF(TRIM(traffic_medium), '') AS traffic_medium,
        NULLIF(TRIM(traffic_campaign), '') AS traffic_campaign
    FROM events
    WHERE user_pseudo_id IS NOT NULL
      AND ga_session_id IS NOT NULL
),

session_data AS (
    SELECT
        user_pseudo_id,
        ga_session_id,
        MIN(traffic_source) AS traffic_source,
        MIN(traffic_medium) AS traffic_medium,
        MIN(traffic_campaign) AS traffic_campaign,
        MAX(CASE WHEN event_name = 'purchase' THEN 1 ELSE 0 END)
            AS converted
    FROM event_data
    GROUP BY user_pseudo_id, ga_session_id
),

acquisition_summary AS (
    SELECT
        COALESCE(traffic_source, '(missing)') AS traffic_source,
        COALESCE(traffic_medium, '(missing)') AS traffic_medium,
        COALESCE(traffic_campaign, '(missing)') AS traffic_campaign,
        COUNT(*) AS sessions,
        SUM(converted) AS converting_sessions
    FROM session_data
    GROUP BY 1, 2, 3
)

SELECT
    traffic_source,
    traffic_medium,
    traffic_campaign,
    sessions,
    converting_sessions,
    ROUND(
        100.0 * converting_sessions / NULLIF(sessions, 0),
        2
    ) AS session_conversion_rate_pct
FROM acquisition_summary
ORDER BY sessions DESC;
