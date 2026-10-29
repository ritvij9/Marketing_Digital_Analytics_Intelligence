
-- Diagnose acquisition metadata conflicts within sessions.
-- Returns one row per session with at least one conflicting field.

WITH event_acquisition AS (
    SELECT
        user_pseudo_id,
        ga_session_id,
        NULLIF(TRIM(event_source), '') AS event_source,
        NULLIF(TRIM(event_medium), '') AS event_medium,
        NULLIF(TRIM(event_campaign), '') AS event_campaign
    FROM events
    WHERE user_pseudo_id IS NOT NULL
      AND ga_session_id IS NOT NULL
),

session_values AS (
    SELECT
        user_pseudo_id,
        ga_session_id,

        COUNT(DISTINCT event_source) AS distinct_sources,
        COUNT(DISTINCT event_medium) AS distinct_mediums,
        COUNT(DISTINCT event_campaign) AS distinct_campaigns,

        STRING_AGG(DISTINCT event_source, ' | ' ORDER BY event_source)
            AS source_values,
        STRING_AGG(DISTINCT event_medium, ' | ' ORDER BY event_medium)
            AS medium_values,
        STRING_AGG(DISTINCT event_campaign, ' | ' ORDER BY event_campaign)
            AS campaign_values

    FROM event_acquisition
    GROUP BY user_pseudo_id, ga_session_id
)

SELECT
    user_pseudo_id,
    ga_session_id,
    distinct_sources,
    distinct_mediums,
    distinct_campaigns,
    source_values,
    medium_values,
    campaign_values
FROM session_values
WHERE distinct_sources > 1
   OR distinct_mediums > 1
   OR distinct_campaigns > 1
ORDER BY
    distinct_sources DESC,
    distinct_mediums DESC,
    distinct_campaigns DESC,
    user_pseudo_id,
    ga_session_id;
