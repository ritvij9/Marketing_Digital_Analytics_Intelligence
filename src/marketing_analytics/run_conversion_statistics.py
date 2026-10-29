
"""Generate confidence intervals for acquisition conversion rates."""

from pathlib import Path

import pandas as pd

from marketing_analytics.conversion_statistics import (
    add_conversion_uncertainty,
)


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]

    input_path = (
        project_root
        / "data"
        / "processed"
        / "session_acquisition_conversion_20210101_20210107.csv"
    )

    output_path = (
        project_root
        / "data"
        / "processed"
        / "acquisition_conversion_uncertainty_20210101_20210107.csv"
    )

    if not input_path.is_file():
        raise FileNotFoundError(
            f"Input report not found: {input_path}"
        )

    results = pd.read_csv(input_path)

    report = add_conversion_uncertainty(
        results,
        minimum_sessions=200,
    )

    report = report.sort_values(
        "conversion_rate_pct",
        ascending=False,
    )

    report.to_csv(output_path, index=False)

    display_columns = [
        "traffic_source",
        "traffic_medium",
        "traffic_campaign",
        "sessions",
        "converting_sessions",
        "conversion_rate_pct",
        "ci_lower_pct",
        "ci_upper_pct",
        "sample_size_status",
    ]

    print(report[display_columns].to_string(index=False))
    print(f"\nReport saved to: {output_path}")


if __name__ == "__main__":
    main()
