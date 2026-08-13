"""Tests for the FedTrust evaluation runner."""

from fedtrust.core.models import (
    EvaluationContext,
    EvaluationReport,
    EvaluationStatus,
    MetricResult,
)
from fedtrust.core.protocols import Evaluator
from fedtrust.core.runner import EvaluationRunner


class SuccessfulEvaluator:
    """Evaluator that returns a successful deterministic evaluation report."""

    @property
    def name(self) -> str:
        """Return the evaluator name."""
        return "successful"

    def evaluate(self, context: EvaluationContext) -> EvaluationReport:
        """Return a successful evaluation report."""
        return EvaluationReport(
            name=self.name,
            status=EvaluationStatus.SUCCESS,
            metrics=[
                MetricResult(name="accuracy", value=1.0),
            ],
        )


class FailingEvaluator:
    """Evaluator that raises an exception during evaluation."""

    @property
    def name(self) -> str:
        """Return the evaluator name."""
        return "failing"

    def evaluate(self, context: EvaluationContext) -> EvaluationReport:
        """Raise a deterministic evaluation error."""
        raise RuntimeError("Evaluation failed")


def test_runner_returns_successful_report() -> None:
    """Runner returns a successful evaluation report with execution duration."""
    runner = EvaluationRunner()
    evaluator = SuccessfulEvaluator()

    context = EvaluationContext(
        model_name="test_model",
        dataset_name="test_dataset",
    )

    report = runner.run(evaluator, context)

    assert isinstance(evaluator, Evaluator)
    assert report.status == EvaluationStatus.SUCCESS
    assert report.metrics[0].name == "accuracy"
    assert report.duration_seconds is not None
    assert report.duration_seconds >= 0


def test_runner_converts_exception_to_failed_report() -> None:
    """Runner converts evaluation exceptions into structured failed evaluation reports."""
    runner = EvaluationRunner()
    evaluator = FailingEvaluator()

    context = EvaluationContext(
        model_name="test_model",
        dataset_name="test_dataset",
    )

    report = runner.run(evaluator, context)

    assert report.name == "failing"
    assert report.status == EvaluationStatus.FAILED
    assert report.error == "Evaluation failed"
    assert report.duration_seconds is not None
    assert report.duration_seconds >= 0
