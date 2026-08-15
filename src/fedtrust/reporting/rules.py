"""Assessment rules for interpreting FedTrust evaluation metrics."""

from fedtrust.core.models import MetricResult
from fedtrust.reporting.models import (
    AssessmentSeverity,
    Finding,
    Recommendation,
)


def assess_metric(metric: MetricResult) -> tuple[Finding | None, Recommendation | None]:
    """Interpret a metric and optionally return a finding and recommendation."""
    if metric.name == "mia_auc":
        return _assess_mia_auc(metric)

    if metric.name == "accuracy":
        return _assess_accuracy(metric)

    return None, None


def _assess_mia_auc(metric: MetricResult) -> tuple[Finding | None, Recommendation | None]:
    """Assess membership inference attack AUC."""
    if metric.value < 0.55:
        return None, None

    if metric.value < 0.65:
        severity = AssessmentSeverity.MEDIUM
        title = "Elevated membership leakage"
        description = (
            "The evaluation indicates that membership inference performs "
            "better than near-random discrimination."
        )
        recommendation = "Evaluate additional privacy protection."

    elif metric.value < 0.80:
        severity = AssessmentSeverity.HIGH
        title = "Significant membership leakage"
        description = "The model shows substantial membership information leakage."
        recommendation = "Evaluate privacy-preserving training and compare privacy with utility."

    else:
        severity = AssessmentSeverity.CRITICAL
        title = "Critical membership leakage"
        description = (
            "The evaluation indicates that membership status can be "
            "distinguished with high effectiveness."
        )
        recommendation = "Prioritize privacy mitigation before deployment."

    finding = Finding(
        title=title,
        description=description,
        severity=severity,
        evidence=[f"MIA AUC = {metric.value:.3f}"],
    )

    recommendation_model = Recommendation(
        title="Improve privacy protection",
        description=recommendation,
        priority=severity,
    )

    return finding, recommendation_model


def _assess_accuracy(
    metric: MetricResult,
) -> tuple[Finding | None, Recommendation | None]:
    """Assess classification accuracy."""
    if metric.value >= 0.90:
        return None, None

    if metric.value >= 0.75:
        severity = AssessmentSeverity.MEDIUM
        title = "Moderate model performance"
        description = "The model achieves acceptable but improvable predictive performance."
        recommendation = "Review model performance before production deployment."
    elif metric.value >= 0.60:
        severity = AssessmentSeverity.HIGH
        title = "Low model performance"
        description = "The model shows limited predictive performance."
        recommendation = "Investigate model quality and training configuration."
    else:
        severity = AssessmentSeverity.CRITICAL
        title = "Critical model performance issue"
        description = "The model demonstrates poor predictive performance."
        recommendation = "Do not rely on the model without substantial improvement."

    finding = Finding(
        title=title,
        description=description,
        severity=severity,
        evidence=[f"Accuracy = {metric.value:.3f}"],
    )

    recommendation_model = Recommendation(
        title="Improve model performance",
        description=recommendation,
        priority=severity,
    )

    return finding, recommendation_model
