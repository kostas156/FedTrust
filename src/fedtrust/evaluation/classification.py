"""Classification evaluation components for the FedTrust framework."""

from collections.abc import Sequence

from fedtrust.core.models import (
    EvaluationContext,
    EvaluationReport,
    EvaluationStatus,
    MetricResult,
)


class ClassificationEvaluator:
    """Evaluate classification predictions against ground truth labels."""

    @property
    def name(self) -> str:
        """Return the name of the evaluator."""
        return "classification"

    def __init__(self, y_true: Sequence[int], y_pred: Sequence[int]) -> None:
        """Initialize the evaluator with labels and predictions."""
        self._y_true = y_true
        self._y_pred = y_pred

    def evaluate(self, context: EvaluationContext) -> EvaluationReport:
        """Calculate classification performance metrics and return an evaluation report."""
        if len(self._y_true) != len(self._y_pred):
            return EvaluationReport(
                name=self.name,
                status=EvaluationStatus.FAILED,
                error="Ground truth and predictions must have the same length.",
            )

        if not self._y_true:
            return EvaluationReport(
                name=self.name,
                status=EvaluationStatus.FAILED,
                error="Evaluation data cannot be empty.",
            )

        correct_predictions = sum(
            true_label == predicted_label
            for true_label, predicted_label in zip(self._y_true, self._y_pred, strict=True)
        )

        accuracy = correct_predictions / len(self._y_true)

        return EvaluationReport(
            name=self.name,
            status=EvaluationStatus.SUCCESS,
            metrics=[
                MetricResult(name="accuracy", value=accuracy, unit="ratio", higher_is_better=True),
            ],
            metadata={
                "model_name": context.model_name,
                "dataset_name": context.dataset_name,
                "sample_size": len(self._y_true),
            },
        )
