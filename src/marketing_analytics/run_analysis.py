"""Run the local GA4 session funnel analysis."""

from pathlib import Path

from marketing_analytics.database import run_session_funnel
from marketing_analytics.ingestion import load_ga4_events


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    input_path = (
        project_root
        / "data"
        / "raw"
        / "ga4_events_20210101_20210107.csv"
    )
    output_path = (
        project_root
        / "data"
        / "processed"
        / "session_funnel_20210101_20210107.csv"
    )

    events = load_ga4_events(input_path)
    funnel = run_session_funnel(events)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    funnel.to_csv(output_path, index=False)

    print(f"Input events: {len(events):,}")
    print(f"Distinct users: {events['user_pseudo_id'].nunique():,}")
    print(
        "Distinct sessions: "
        f"{events.drop_duplicates(['user_pseudo_id', 'ga_session_id']).shape[0]:,}"
    )
    print("\nSession funnel:")
    print(funnel.to_string(index=False))
    print(f"\nSaved results to: {output_path}")


if __name__ == "__main__":
    main()
