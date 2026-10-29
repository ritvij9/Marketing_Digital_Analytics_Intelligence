
-- Session-level acquisition summary using GA4 traffic_source fields.
-- Each session is assigned one distinct combination only if its events
-- agree on that combination. Conflicting combinations are flagged separately.

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

        COUNT(
            DISTINCT (
                traffic_source,
                traffic_medium,
                traffic_campaign
            )
        ) FILTER (
            WHERE traffic_source IS NOT NULL
               OR traffic_medium IS NOT NULL
               OR traffic_campaign IS NOT NULL
        ) AS distinct_source_combinations,

        MIN(traffic_source) AS traffic_source,
        MIN(traffic_medium) AS traffic_medium,
        MIN(traffic_campaign) AS traffic_campaign,

        COUNT(*) FILTER (
            WHERE traffic_source IS NOT NULL
               OR traffic_medium IS NOT NULL
               OR traffic_campaign IS NOT NULL
        ) AS events_with_traffic_source

    FROM event_sources
    GROUP BY user_pseudo_id, ga_session_id
),

classified_sessions AS (
    SELECT
        *,
        CASE
            WHEN events_with_traffic_source = 0 THEN 'missing'
            WHEN distinct_source_combinations > 1 THEN 'conflicting'
            ELSE 'consistent'
        END AS attribution_status
    FROM session_sources
)

SELECT
    attribution_status,
    COUNT(*) AS sessions
FROM classified_sessions
GROUP BY attribution_status
ORDER BY attribution_status;
