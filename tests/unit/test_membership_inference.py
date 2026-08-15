"""Tests for the FedTrust membership inference evaluator."""

from fedtrust.core.models import EvaluationContext, EvaluationStatus
from fedtrust.privacy.membership_inference import MembershipInferenceEvaluator


def test_membership_inference_evaluator_calculates_auc() -> None:
    """MIA evaluator calculates the expected ROC-AUC."""
    evaluator = MembershipInferenceEvaluator(
        membership_labels=[1, 1, 0, 0],
        attack_scores=[0.9, 0.8, 0.2, 0.1],
    )

    context = EvaluationContext(
        model_name="baseline_model",
        dataset_name="prvacy_dataset",
    )

    report = evaluator.evaluate(context)

    assert report.status is EvaluationStatus.SUCCESS
    assert report.metrics[0].name == "mia_auc"
    assert report.metrics[0].value == 1.0
    assert report.metrics[0].higher_is_better is False
    assert report.metadata["member_count"] == 2
    assert report.metadata["non_member_count"] == 2


def test_membership_inference_evaluator_rejects_mismatched_lengths() -> None:
    """MIA evaluator rejects mismatched labels and scores."""
    evaluator = MembershipInferenceEvaluator(
        membership_labels=[1, 1, 0],
        attack_scores=[0.9, 0.8],
    )

    context = EvaluationContext(
        model_name="baseline_model",
        dataset_name="prvacy_dataset",
    )

    report = evaluator.evaluate(context)

    assert report.status is EvaluationStatus.FAILED
    assert report.error == "Membership labels and attack scores must have the same length."


def test_membership_inference_evaluator_rejects_empty_inputs() -> None:
    """MIA evaluator rejects empty evaluation data."""
    evaluator = MembershipInferenceEvaluator(
        membership_labels=[],
        attack_scores=[],
    )

    context = EvaluationContext(
        model_name="baseline_model",
        dataset_name="prvacy_dataset",
    )

    report = evaluator.evaluate(context)

    assert report.status is EvaluationStatus.FAILED
    assert report.error == "Evaluation data cannot be empty."


def test_membership_inference_evaluator_requires_both_classes() -> None:
    """MIA evaluator requires both members and non-members."""
    evaluator = MembershipInferenceEvaluator(
        membership_labels=[1, 1, 1, 1],
        attack_scores=[0.9, 0.8, 0.7, 0.6],
    )

    context = EvaluationContext(
        model_name="baseline_model",
        dataset_name="prvacy_dataset",
    )

    report = evaluator.evaluate(context)

    assert report.status is EvaluationStatus.FAILED
    assert (
        report.error == "Membership labels must contain both 0 and 1 classes for AUC calculation."
    )
