"""Generate a demonstration FedTrust assessment report."""

from pathlib import Path

from fedtrust.core.models import EvaluationContext
from fedtrust.core.runner import EvaluationRunner
from fedtrust.evaluation.classification import ClassificationEvaluator
from fedtrust.privacy.membership_inference import MembershipInferenceEvaluator
from fedtrust.reporting.builder import AssessmentBuilder
from fedtrust.reporting.chart_generator import ChartGenerator
from fedtrust.reporting.charts import ChartSpecification, ChartType
from fedtrust.reporting.docx_renderer import DocxRenderer


def main() -> None:
    """Run the complete demonstration reporting pipeline."""
    output_dir = Path("examples/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    context = EvaluationContext(
        model_name="demo-model",
        dataset_name="demo-dataset",
        evaluation_metadata={
            "purpose": "FedTrust Day 5 demonstration",
        },
    )

    classification_evaluator = ClassificationEvaluator(
        y_true=[0, 1, 1, 0, 1],
        y_pred=[0, 1, 0, 0, 1],
    )

    membership_labels = [1, 1, 0, 0]
    attack_scores = [0.9, 0.8, 0.2, 0.1]

    mia_evaluator = MembershipInferenceEvaluator(
        membership_labels=membership_labels,
        attack_scores=attack_scores,
    )

    runner = EvaluationRunner()

    classification_report = runner.run(
        classification_evaluator,
        context,
    )

    mia_report = runner.run(
        mia_evaluator,
        context,
    )

    evaluation_reports = [
        classification_report,
        mia_report,
    ]

    assessment = AssessmentBuilder().build(evaluation_reports)

    mia_chart_path = output_dir / "mia_roc.png"

    ChartGenerator().generate(
        ChartSpecification(
            chart_type=ChartType.ROC_CURVE,
            title="Membership Inference ROC Curve",
            caption=(
                "ROC curve showing the ability of the membership "
                "inference attack to distinguish members from non-members."
            ),
            data={
                "labels": membership_labels,
                "scores": attack_scores,
            },
        ),
        mia_chart_path,
    )

    report_path = output_dir / "FedTrust_Assessment.docx"

    DocxRenderer().render(
        assessment,
        report_path,
        chart_paths={
            "membership_inference": mia_chart_path,
        },
    )

    print(f"Assessment generated: {report_path}")


if __name__ == "__main__":
    main()
