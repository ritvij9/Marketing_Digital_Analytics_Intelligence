-- Count distinct sessions containing each event.
-- This measures event presence, not sequential conversion.

WITH funnel_events AS (
    SELECT *
    FROM (
        VALUES
            ('page_view', 1),
            ('view_item', 2),
            ('add_to_cart', 3),
            ('begin_checkout', 4),
            ('add_shipping_info', 5),
            ('add_payment_info', 6),
            ('purchase', 7)
    ) AS t(event_name, event_order)
),

session_event_presence AS (
    SELECT DISTINCT
        user_pseudo_id,
        ga_session_id,
        event_name
    FROM events
    WHERE user_pseudo_id IS NOT NULL
      AND ga_session_id IS NOT NULL
)

SELECT
    f.event_name,
    COUNT(s.event_name) AS sessions
FROM funnel_events AS f
LEFT JOIN session_event_presence AS s
    ON f.event_name = s.event_name
GROUP BY f.event_name, f.event_order
ORDER BY f.event_order;
