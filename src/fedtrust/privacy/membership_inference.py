"""Membership inference evaluation module for FedTrust."""

from collections.abc import Sequence

from sklearn.metrics import roc_auc_score

from fedtrust.core.models import (
    EvaluationContext,
    EvaluationReport,
    EvaluationStatus,
    MetricResult,
)


class MembershipInferenceEvaluator:
    """Evaluate membership inference attack scores."""

    @property
    def name(self) -> str:
        """Return the name of the evaluator."""
        return "membership_inference"

    def __init__(self, membership_labels: Sequence[int], attack_scores: Sequence[float]) -> None:
        """Initialize the evaluator with membership labels and attack scores."""
        self._membership_labels = membership_labels
        self._attack_scores = attack_scores

    def evaluate(self, context: EvaluationContext) -> EvaluationReport:
        """Calculate membership inference performance."""
        if len(self._membership_labels) != len(self._attack_scores):
            return EvaluationReport(
                name=self.name,
                status=EvaluationStatus.FAILED,
                error="Membership labels and attack scores must have the same length.",
            )

        if not self._membership_labels:
            return EvaluationReport(
                name=self.name,
                status=EvaluationStatus.FAILED,
                error="Evaluation data cannot be empty.",
            )

        if set(self._membership_labels) != {0, 1}:
            return EvaluationReport(
                name=self.name,
                status=EvaluationStatus.FAILED,
                error="Membership labels must contain both 0 and 1 classes for AUC calculation.",
            )

        try:
            auc_score = float(roc_auc_score(self._membership_labels, self._attack_scores))
        except ValueError as exc:
            return EvaluationReport(
                name=self.name,
                status=EvaluationStatus.FAILED,
                error=f"Error calculating AUC: {str(exc)}",
            )

        return EvaluationReport(
            name=self.name,
            status=EvaluationStatus.SUCCESS,
            metrics=[
                MetricResult(
                    name="mia_auc", value=auc_score, unit="roc_auc", higher_is_better=False
                )
            ],
            metadata={
                "model_name": context.model_name,
                "dataset_name": context.dataset_name,
                "sample_size": len(self._membership_labels),
                "member_count": sum(label == 1 for label in self._membership_labels),
                "non_member_count": sum(label == 0 for label in self._membership_labels),
            },
        )
