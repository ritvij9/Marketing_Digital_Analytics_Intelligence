
"""Statistical utilities for session conversion analysis."""

import pandas as pd
from statsmodels.stats.proportion import proportion_confint


def add_conversion_uncertainty(
    results: pd.DataFrame,
    minimum_sessions: int = 200,
    alpha: float = 0.05,
) -> pd.DataFrame:
    """Add Wilson confidence intervals and sample-size flags.

    Required columns:
        sessions
        converting_sessions

    Confidence intervals are calculated for each group's conversion rate.
    """
    if minimum_sessions < 1:
        raise ValueError("minimum_sessions must be at least 1.")

    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1.")

    required_columns = {"sessions", "converting_sessions"}
    missing_columns = required_columns - set(results.columns)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")

    if results.empty:
        raise ValueError("Results must not be empty.")

    output = results.copy()

    if (output["sessions"] <= 0).any():
        raise ValueError("Session counts must be positive.")

    if (
        (output["converting_sessions"] < 0)
        | (output["converting_sessions"] > output["sessions"])
    ).any():
        raise ValueError(
            "Converting sessions must be between zero and total sessions."
        )

    intervals = [
        proportion_confint(
            count=int(row.converting_sessions),
            nobs=int(row.sessions),
            alpha=alpha,
            method="wilson",
        )
        for row in output.itertuples()
    ]

    output["conversion_rate_pct"] = (
        100 * output["converting_sessions"] / output["sessions"]
    ).round(3)

    output["ci_lower_pct"] = [
        round(lower * 100, 3) for lower, _ in intervals
    ]
    output["ci_upper_pct"] = [
        round(upper * 100, 3) for _, upper in intervals
    ]

    output["sample_size_status"] = output["sessions"].apply(
        lambda count: (
            "sufficient_for_screening"
            if count >= minimum_sessions
            else "small_sample"
        )
    )

    return output
