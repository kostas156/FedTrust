"""Tests for the FedTrust DOCX renderer."""

from pathlib import Path

from docx import Document

from fedtrust.reporting.docx_renderer import DocxRenderer
from fedtrust.reporting.models import (
    AssessmentReport,
    AssessmentSection,
    AssessmentSeverity,
    Finding,
    Recommendation,
)


def test_docx_renderer_creates_report(tmp_path: Path) -> None:
    """Renderer creates a valid DOCX assessment report."""
    report = AssessmentReport(
        title="FedTrust Trustworthiness Assessment",
        executive_summary="The model requires privacy improvements.",
        overall_severity=AssessmentSeverity.HIGH,
        sections=[
            AssessmentSection(
                name="Privacy",
                summary="Privacy leakage was identified.",
                findings=[
                    Finding(
                        title="Membership leakage",
                        description="The attack detects training membership.",
                        severity=AssessmentSeverity.HIGH,
                        evidence=["MIA AUC = 0.72"],
                    ),
                ],
                recommendations=[
                    Recommendation(
                        title="Evaluate DP training",
                        description="Compare stronger privacy protection.",
                        priority=AssessmentSeverity.HIGH,
                    ),
                ],
                metrics=[
                    {
                        "name": "mia_auc",
                        "value": 0.72,
                        "unit": "roc_auc",
                    },
                ],
            ),
        ],
        metadata={
            "model": "baseline-model",
            "dataset": "privacy-dataset",
        },
    )

    output_path = tmp_path / "assessment.docx"

    generated_path = DocxRenderer().render(
        report,
        output_path,
    )

    assert generated_path == output_path
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_docx_renderer_embeds_chart(
    tmp_path: Path,
) -> None:
    """Renderer embeds a supplied chart into the DOCX document."""
    from fedtrust.reporting.chart_generator import ChartGenerator
    from fedtrust.reporting.charts import ChartSpecification, ChartType

    chart_path = tmp_path / "mia_roc.png"

    ChartGenerator().generate(
        ChartSpecification(
            chart_type=ChartType.ROC_CURVE,
            title="Membership Inference ROC Curve",
            data={
                "labels": [1, 1, 0, 0],
                "scores": [0.9, 0.8, 0.2, 0.1],
            },
        ),
        chart_path,
    )

    report = AssessmentReport(
        title="FedTrust Trustworthiness Assessment",
        executive_summary="Privacy assessment.",
        overall_severity=AssessmentSeverity.HIGH,
        sections=[
            AssessmentSection(
                name="membership_inference",
                summary="Membership inference assessment.",
            ),
        ],
    )

    output_path = tmp_path / "assessment_with_chart.docx"

    DocxRenderer().render(
        report,
        output_path,
        chart_paths={"membership_inference": chart_path},
    )

    document = Document(output_path)

    assert output_path.exists()
    assert len(document.inline_shapes) == 1
