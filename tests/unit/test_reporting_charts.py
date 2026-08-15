"""Tests for FedTrust chart generation."""

from pathlib import Path

from fedtrust.reporting.chart_generator import ChartGenerator
from fedtrust.reporting.charts import ChartSpecification, ChartType


def test_generate_roc_curve(tmp_path: Path) -> None:
    """ROC chart generator creates an image artifact."""
    specification = ChartSpecification(
        chart_type=ChartType.ROC_CURVE,
        title="Membership Inference ROC Curve",
        data={
            "labels": [1, 1, 0, 0],
            "scores": [0.9, 0.8, 0.2, 0.1],
        },
    )

    output_path = tmp_path / "mia_roc.png"

    generated_path = ChartGenerator().generate(
        specification,
        output_path,
    )

    assert generated_path == output_path
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_generate_bar_chart(tmp_path: Path) -> None:
    """Bar chart generator creates an image artifact."""
    specification = ChartSpecification(
        chart_type=ChartType.BAR,
        title="Model Performance",
        data={
            "labels": ["Accuracy"],
            "values": [0.80],
        },
    )

    output_path = tmp_path / "performance.png"

    generated_path = ChartGenerator().generate(
        specification,
        output_path,
    )

    assert generated_path == output_path
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_roc_curve_requires_labels_and_scores(tmp_path: Path) -> None:
    """ROC chart generation rejects incomplete data."""
    specification = ChartSpecification(
        chart_type=ChartType.ROC_CURVE,
        title="Invalid ROC",
    )

    output_path = tmp_path / "invalid.png"

    try:
        ChartGenerator().generate(
            specification,
            output_path,
        )
    except ValueError as exc:
        assert "labels" in str(exc)
        assert "scores" in str(exc)
    else:
        raise AssertionError("Expected ValueError was not raised.")
