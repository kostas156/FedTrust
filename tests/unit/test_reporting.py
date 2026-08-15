"""Test for FedTrust assessment reporting models."""

from fedtrust.reporting.models import (
    AssessmentReport,
    AssessmentSection,
    AssessmentSeverity,
    Finding,
    Recommendation,
)


def test_finding_stores_evidence_and_severity() -> None:
    """Findings store structured evidence and severity."""
    finding = Finding(
        title="Elevated membership leakage",
        description="The model shows measurable privacy leakage.",
        severity=AssessmentSeverity.HIGH,
        evidence=["MIA AUC = 0.72"],
    )

    assert finding.severity is AssessmentSeverity.HIGH
    assert finding.evidence == ["MIA AUC = 0.72"]


def test_recommendation_has_default_priority() -> None:
    """Recommendations use medium priority by default."""
    recommendation = Recommendation(
        title="Evaluate differential privacy",
        description="Compare privacy protection against model utility.",
    )

    assert recommendation.priority is AssessmentSeverity.MEDIUM


def test_assessment_section_groups_findings_and_recommendations() -> None:
    """Assessment sections group related assessment information."""
    section = AssessmentSection(
        name="Privacy",
        summary="The model shows measurable privacy leakage.",
        findings=[
            Finding(
                title="Membership leakage",
                description="The attack separates members from non-members.",
                severity=AssessmentSeverity.HIGH,
            ),
        ],
        recommendations=[
            Recommendation(
                title="Evaluate DP training",
                description="Measure the privacy-utility trade-off.",
                priority=AssessmentSeverity.HIGH,
            ),
        ],
        metrics=[
            {
                "name": "mia_auc",
                "value": 0.72,
            },
        ],
    )

    assert section.name == "Privacy"
    assert len(section.findings) == 1
    assert len(section.recommendations) == 1
    assert section.metrics[0]["name"] == "mia_auc"


def test_assessment_report_groups_sections() -> None:
    """Assessment reports provide a canonical top-level structure."""
    report = AssessmentReport(
        title="FedTrust Trustworthiness Assessment",
        executive_summary="The system shows strong utility with elevated privacy risk.",
        overall_severity=AssessmentSeverity.HIGH,
        sections=[
            AssessmentSection(
                name="Privacy",
                summary="Privacy leakage requires attention.",
            ),
        ],
        metadata={
            "model": "baseline-model",
            "dataset": "privacy-dataset",
        },
    )

    assert report.overall_severity is AssessmentSeverity.HIGH
    assert len(report.sections) == 1
    assert report.sections[0].name == "Privacy"
    assert report.metadata["model"] == "baseline-model"
