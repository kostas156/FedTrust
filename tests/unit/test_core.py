"""Tests for FedTrust core domain models."""

from fedtrust.core.models import (
    EvaluationContext,
    EvaluationReport,
    EvaluationStatus,
    MetricResult,
)
from fedtrust.core.protocols import Evaluator


class DummyEvaluator:
    """Minimal evaluator used for testing the Evaluator protocol."""

    @property
    def name(self) -> str:
        """Return the name of the evaluator."""
        return "dummy_evaluator"

    def evaluate(self, context: EvaluationContext) -> EvaluationReport:
        """Returning a deterministic evaluation report."""
        return EvaluationReport(
            name=self.name,
            status=EvaluationStatus.SUCCESS,
            metrics=[
                MetricResult(name="accuracy", value=1.0),
            ],
        )


def test_evaluator_protocol() -> None:
    """Concrete evaluators conform to the Evaluator protocol."""
    evaluator = DummyEvaluator()

    assert isinstance(evaluator, Evaluator)

    context = EvaluationContext(
        model_name="test_model",
        dataset_name="test_dataset",
    )

    report = evaluator.evaluate(context)

    assert report.name == "dummy_evaluator"
    assert report.status == EvaluationStatus.SUCCESS
    assert report.metrics[0].value == 1.0


def test_metric_result() -> None:
    """Metric results store structured metric information."""
    metric = MetricResult(
        name="accuracy",
        value=0.95,
        unit="ratio",
        higher_is_better=True,
    )

    assert metric.name == "accuracy"
    assert metric.value == 0.95
    assert metric.unit == "ratio"


def test_evaluation_report() -> None:
    """Evaluation reports contain structured metric results."""
    report = EvaluationReport(
        name="baseline_evaluation",
        status=EvaluationStatus.SUCCESS,
        metrics=[
            MetricResult(name="accuracy", value=0.95),
        ],
    )

    assert report.status == EvaluationStatus.SUCCESS
    assert len(report.metrics) == 1
    assert report.metrics[0].name == "accuracy"


def test_evaluation_status_serializes_as_string() -> None:
    """Evaluation status values serialize as strings."""
    report = EvaluationReport(
        name="baseline_evaluation",
        status=EvaluationStatus.SUCCESS,
    )

    assert report.model_dump()["status"] == "success"


def test_evaluation_context() -> None:
    """Evaluation contexts store model and dataset information."""
    context = EvaluationContext(
        model_name="baseline_model",
        dataset_name="adult_census",
        model_metadata={"architecture": "mlp"},
        dataset_metadata={"sample_size": 48842},
        evaluation_metadata={"seed": 42},
    )

    assert context.model_name == "baseline_model"
    assert context.dataset_name == "adult_census"
    assert context.model_metadata["architecture"] == "mlp"
    assert context.dataset_metadata["sample_size"] == 48842
    assert context.evaluation_metadata["seed"] == 42
