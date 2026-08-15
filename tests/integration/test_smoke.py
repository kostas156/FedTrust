"""Integration smoke tests."""

import fedtrust
from fedtrust.core.models import EvaluationContext, EvaluationStatus
from fedtrust.core.runner import EvaluationRunner
from fedtrust.evaluation.classification import ClassificationEvaluator
from fedtrust.privacy.membership_inference import MembershipInferenceEvaluator


def test_package_import() -> None:
    """Package can be imported without errors."""
    assert fedtrust is not None
    assert hasattr(fedtrust, "__version__")


def test_classification_evaluation_pipeline() -> None:
    """Classification evaluator works through the evaluation runner."""
    evaluator = ClassificationEvaluator(
        y_true=[0, 1, 1, 0, 1],
        y_pred=[0, 1, 0, 0, 1],
    )

    context = EvaluationContext(
        model_name="integration_test_model",
        dataset_name="integration_test_dataset",
    )

    runner = EvaluationRunner()
    report = runner.run(evaluator, context)

    assert report.status == EvaluationStatus.SUCCESS
    assert report.name == "classification"
    assert report.metrics[0].name == "accuracy"
    assert report.metrics[0].value == 0.8
    assert report.metadata["model_name"] == "integration_test_model"
    assert report.metadata["dataset_name"] == "integration_test_dataset"
    assert report.metadata["sample_size"] == 5
    assert report.duration_seconds is not None
    assert report.duration_seconds >= 0


def test_membership_inference_evaluation_pipeline() -> None:
    """Membership inference evaluator works through the evaluation runner."""
    evaluator = MembershipInferenceEvaluator(
        membership_labels=[1, 1, 0, 0],
        attack_scores=[0.9, 0.8, 0.2, 0.1],
    )

    context = EvaluationContext(
        model_name="privacy_integration_test_model",
        dataset_name="privacy_integration_test_dataset",
    )

    runner = EvaluationRunner()
    report = runner.run(evaluator, context)

    assert report.status == EvaluationStatus.SUCCESS
    assert report.name == "membership_inference"
    assert report.metrics[0].name == "mia_auc"
    assert report.metrics[0].value == 1.0
    assert report.metadata["model_name"] == "privacy_integration_test_model"
    assert report.metadata["dataset_name"] == "privacy_integration_test_dataset"
    assert report.metadata["sample_size"] == 4
    assert report.metadata["member_count"] == 2
    assert report.metadata["non_member_count"] == 2
    assert report.duration_seconds is not None
    assert report.duration_seconds >= 0
