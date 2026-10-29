-- Measure acquisition metadata coverage and consistency at session level.
-- A conflict means a session contains more than one distinct non-empty value.
-- Missing acquisition values are not treated as conflicts.

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

session_quality AS (
    SELECT
        user_pseudo_id,
        ga_session_id,

        COUNT(DISTINCT event_source) AS distinct_sources,
        COUNT(DISTINCT event_medium) AS distinct_mediums,
        COUNT(DISTINCT event_campaign) AS distinct_campaigns,

        MAX(CASE WHEN event_source IS NOT NULL THEN 1 ELSE 0 END)
            AS has_source,
        MAX(CASE WHEN event_medium IS NOT NULL THEN 1 ELSE 0 END)
            AS has_medium,
        MAX(CASE WHEN event_campaign IS NOT NULL THEN 1 ELSE 0 END)
            AS has_campaign

    FROM event_acquisition
    GROUP BY user_pseudo_id, ga_session_id
)

SELECT
    COUNT(*) AS total_sessions,

    SUM(has_source) AS sessions_with_source,
    SUM(has_medium) AS sessions_with_medium,
    SUM(has_campaign) AS sessions_with_campaign,

    SUM(
        CASE
            WHEN has_source = 1
              OR has_medium = 1
              OR has_campaign = 1
            THEN 1 ELSE 0
        END
    ) AS sessions_with_any_acquisition_data,

    SUM(CASE WHEN distinct_sources > 1 THEN 1 ELSE 0 END)
        AS sessions_with_source_conflicts,
    SUM(CASE WHEN distinct_mediums > 1 THEN 1 ELSE 0 END)
        AS sessions_with_medium_conflicts,
    SUM(CASE WHEN distinct_campaigns > 1 THEN 1 ELSE 0 END)
        AS sessions_with_campaign_conflicts,

    SUM(
        CASE
            WHEN distinct_sources > 1
              OR distinct_mediums > 1
              OR distinct_campaigns > 1
            THEN 1 ELSE 0
        END
    ) AS sessions_with_any_acquisition_conflict

FROM session_quality;
