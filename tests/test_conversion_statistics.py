
"""Tests for acquisition conversion uncertainty analysis."""

import pandas as pd
import pytest

from marketing_analytics.conversion_statistics import (
    add_conversion_uncertainty,
)


def test_adds_wilson_confidence_interval():
    results = pd.DataFrame(
        {
            "sessions": [1000],
            "converting_sessions": [10],
        }
    )

    report = add_conversion_uncertainty(results)

    assert report.loc[0, "conversion_rate_pct"] == 1.0
    assert report.loc[0, "ci_lower_pct"] < 1.0
    assert report.loc[0, "ci_upper_pct"] > 1.0
    assert (
        report.loc[0, "sample_size_status"]
        == "sufficient_for_screening"
    )


def test_flags_small_sample():
    results = pd.DataFrame(
        {
            "sessions": [25],
            "converting_sessions": [1],
        }
    )

    report = add_conversion_uncertainty(results)

    assert report.loc[0, "sample_size_status"] == "small_sample"


def test_flags_exact_minimum_sample_size():
    results = pd.DataFrame(
        {
            "sessions": [200],
            "converting_sessions": [2],
        }
    )

    report = add_conversion_uncertainty(results)

    assert (
        report.loc[0, "sample_size_status"]
        == "sufficient_for_screening"
    )


def test_rejects_missing_columns():
    results = pd.DataFrame({"sessions": [100]})

    with pytest.raises(ValueError, match="Missing required columns"):
        add_conversion_uncertainty(results)


def test_rejects_empty_results():
    results = pd.DataFrame(
        columns=["sessions", "converting_sessions"]
    )

    with pytest.raises(ValueError, match="must not be empty"):
        add_conversion_uncertainty(results)


def test_rejects_zero_sessions():
    results = pd.DataFrame(
        {
            "sessions": [0],
            "converting_sessions": [0],
        }
    )

    with pytest.raises(ValueError, match="must be positive"):
        add_conversion_uncertainty(results)


def test_rejects_conversions_greater_than_sessions():
    results = pd.DataFrame(
        {
            "sessions": [10],
            "converting_sessions": [11],
        }
    )

    with pytest.raises(
        ValueError,
        match="must be between zero and total sessions",
    ):
        add_conversion_uncertainty(results)


def test_rejects_invalid_minimum_sessions():
    results = pd.DataFrame(
        {
            "sessions": [100],
            "converting_sessions": [2],
        }
    )

    with pytest.raises(ValueError, match="minimum_sessions"):
        add_conversion_uncertainty(results, minimum_sessions=0)


def test_rejects_invalid_alpha():
    results = pd.DataFrame(
        {
            "sessions": [100],
            "converting_sessions": [2],
        }
    )

    with pytest.raises(ValueError, match="alpha"):
        add_conversion_uncertainty(results, alpha=1.0)
