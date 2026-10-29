
"""Run session conversion analysis by acquisition combination."""

from pathlib import Path

from marketing_analytics.database import run_session_acquisition_conversion
from marketing_analytics.ingestion import load_ga4_events


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]

    input_path = (
        project_root
        / "data"
        / "raw"
        / "ga4_events_traffic_source_20210101_20210107.csv"
    )

    output_path = (
        project_root
        / "data"
        / "processed"
        / "session_acquisition_conversion_20210101_20210107.csv"
    )

    events = load_ga4_events(input_path)
    results = run_session_acquisition_conversion(events)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(output_path, index=False)

    print(f"Input events: {len(events):,}")
    print("\nSession conversion by acquisition combination:")
    print(results.head(15).to_string(index=False))
    print(f"\nSaved results to: {output_path}")


if __name__ == "__main__":
    main()
