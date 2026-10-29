
"""Run the GA4 acquisition-conflict diagnostic."""

from pathlib import Path

from marketing_analytics.database import run_acquisition_conflict_details
from marketing_analytics.ingestion import load_ga4_events


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]

    input_path = (
        project_root
        / "data"
        / "raw"
        / "ga4_events_acquisition_20210101_20210107.csv"
    )

    output_path = (
        project_root
        / "data"
        / "processed"
        / "acquisition_conflict_details_20210101_20210107.csv"
    )

    events = load_ga4_events(input_path)
    conflicts = run_acquisition_conflict_details(events)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    conflicts.to_csv(output_path, index=False)

    print(f"Input events: {len(events):,}")
    print(f"Conflicting sessions: {len(conflicts):,}")
    print("\nFirst 10 conflicting sessions:")

    if conflicts.empty:
        print("No conflicting sessions found.")
    else:
        print(conflicts.head(10).to_string(index=False))

    print(f"\nSaved results to: {output_path}")


if __name__ == "__main__":
    main()
