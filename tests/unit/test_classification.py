"""Tests for the FedTrust classification evaluator."""

from fedtrust.core.models import EvaluationContext, EvaluationStatus
from fedtrust.evaluation.classification import ClassificationEvaluator


def test_classification_evaluator_calculates_accuracy() -> None:
    """ClassificationEvaluator calculates the expected accuracy and returns a successful report."""
    evaluator = ClassificationEvaluator(
        y_true=[0, 1, 1, 0, 1],
        y_pred=[0, 1, 0, 0, 1],
    )

    context = EvaluationContext(
        model_name="baseline_model",
        dataset_name="test_dataset",
    )

    report = evaluator.evaluate(context)

    assert report.status == EvaluationStatus.SUCCESS
    assert report.metrics[0].name == "accuracy"
    assert report.metrics[0].value == 0.8
    assert report.metadata["sample_size"] == 5


def test_classification_evaluator_rejects_mismatched_lengths() -> None:
    """ClassificationEvaluator rejects mismatched input lengths and returns a failed report."""
    evaluator = ClassificationEvaluator(
        y_true=[0, 1, 1],
        y_pred=[0, 1],
    )

    context = EvaluationContext(
        model_name="baseline_model",
        dataset_name="test_dataset",
    )

    report = evaluator.evaluate(context)

    assert report.status == EvaluationStatus.FAILED
    assert report.error == "Ground truth and predictions must have the same length."


def test_classification_evaluator_rejects_empty_inputs() -> None:
    """ClassificationEvaluator rejects empty evaluation data and returns a failed report."""
    evaluator = ClassificationEvaluator(
        y_true=[],
        y_pred=[],
    )

    context = EvaluationContext(
        model_name="baseline_model",
        dataset_name="test_dataset",
    )

    report = evaluator.evaluate(context)

    assert report.status == EvaluationStatus.FAILED
    assert report.error == "Evaluation data cannot be empty."
