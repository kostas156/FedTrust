"""Tests for the FedTrust assessment builder."""

from fedtrust.core.models import (
    EvaluationReport,
    EvaluationStatus,
    MetricResult,
)
from fedtrust.reporting.builder import AssessmentBuilder
from fedtrust.reporting.models import AssessmentSeverity


def test_builder_creates_mia_finding() -> None:
    """Builder creates a finding for elevated MIA risk."""
    report = EvaluationReport(
        name="membership_inference",
        status=EvaluationStatus.SUCCESS,
        metrics=[
            MetricResult(
                name="mia_auc",
                value=0.72,
                unit="roc_auc",
                higher_is_better=False,
            ),
        ],
    )

    assessment = AssessmentBuilder().build([report])

    assert assessment.overall_severity is AssessmentSeverity.HIGH
    assert assessment.sections[0].findings[0].title == "Significant membership leakage"
    assert assessment.sections[0].findings[0].severity is AssessmentSeverity.HIGH
    assert len(assessment.sections[0].recommendations) == 1


def test_builder_ignores_good_accuracy() -> None:
    """Builder does not create a finding for strong accuracy."""
    report = EvaluationReport(
        name="classification",
        status=EvaluationStatus.SUCCESS,
        metrics=[
            MetricResult(
                name="accuracy",
                value=0.95,
                unit="ratio",
                higher_is_better=True,
            ),
        ],
    )

    assessment = AssessmentBuilder().build([report])

    assert assessment.overall_severity is AssessmentSeverity.INFO
    assert assessment.sections[0].findings == []
    assert assessment.sections[0].recommendations == []


def test_builder_combines_multiple_evaluations() -> None:
    """Builder combines findings from multiple evaluations."""
    reports = [
        EvaluationReport(
            name="classification",
            status=EvaluationStatus.SUCCESS,
            metrics=[
                MetricResult(name="accuracy", value=0.70),
            ],
        ),
        EvaluationReport(
            name="membership_inference",
            status=EvaluationStatus.SUCCESS,
            metrics=[
                MetricResult(name="mia_auc", value=0.85),
            ],
        ),
    ]

    assessment = AssessmentBuilder().build(reports)

    assert len(assessment.sections) == 2
    assert assessment.overall_severity is AssessmentSeverity.CRITICAL
