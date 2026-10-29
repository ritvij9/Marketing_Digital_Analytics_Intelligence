
-- Session-level acquisition distribution.
-- One row per distinct user-session key before aggregation.
-- Uses the structured traffic_source fields from the GA4 export.

WITH event_sources AS (
    SELECT
        user_pseudo_id,
        ga_session_id,
        NULLIF(TRIM(traffic_source), '') AS traffic_source,
        NULLIF(TRIM(traffic_medium), '') AS traffic_medium,
        NULLIF(TRIM(traffic_campaign), '') AS traffic_campaign
    FROM events
    WHERE user_pseudo_id IS NOT NULL
      AND ga_session_id IS NOT NULL
),

session_sources AS (
    SELECT
        user_pseudo_id,
        ga_session_id,
        MIN(traffic_source) AS traffic_source,
        MIN(traffic_medium) AS traffic_medium,
        MIN(traffic_campaign) AS traffic_campaign
    FROM event_sources
    GROUP BY user_pseudo_id, ga_session_id
)

SELECT
    COALESCE(traffic_source, '(missing)') AS traffic_source,
    COALESCE(traffic_medium, '(missing)') AS traffic_medium,
    COALESCE(traffic_campaign, '(missing)') AS traffic_campaign,
    COUNT(*) AS sessions,
    ROUND(
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
        2
    ) AS session_percentage
FROM session_sources
GROUP BY 1, 2, 3
ORDER BY sessions DESC;
