"""Generate visual charts for FedTrust reports."""

from pathlib import Path

import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve

from fedtrust.reporting.charts import ChartSpecification, ChartType


class ChartGenerator:
    """Generate chart artifacts from chart specifications."""

    def generate(self, specification: ChartSpecification, output_path: Path) -> Path:
        """Generate a chart and save it to the requested path."""
        if specification.chart_type is ChartType.ROC_CURVE:
            return self._generate_roc_curve(specification, output_path)

        if specification.chart_type is ChartType.BAR:
            return self._generate_bar_chart(specification, output_path)

        raise ValueError(f"Unsupported chart type: {specification.chart_type}")

    @staticmethod
    def _generate_roc_curve(specification: ChartSpecification, output_path: Path) -> Path:
        """Generate and save an ROC curve chart."""
        labels = specification.data.get("labels")
        scores = specification.data.get("scores")

        if labels is None or scores is None:
            raise ValueError("ROC curve data must contain 'labels' and 'scores'.")

        false_positive_rate, true_positive_rate, _ = roc_curve(labels, scores)

        figure, axis = plt.subplots(figsize=(7, 5))
        axis.plot(false_positive_rate, true_positive_rate, label="Membership inference attack")
        axis.plot([0, 1], [0, 1], linestyle="--", label="Random baseline")

        axis.set_title(specification.title)
        axis.set_xlabel("False Positive Rate")
        axis.set_ylabel("True Positive Rate")
        axis.set_xlim(0, 1)
        axis.set_ylim(0, 1)
        axis.legend()
        axis.grid(True, alpha=0.3)

        figure.tight_layout()
        figure.savefig(output_path, dpi=160, bbox_inches="tight")
        plt.close(figure)

        return output_path

    @staticmethod
    def _generate_bar_chart(
        specification: ChartSpecification,
        output_path: Path,
    ) -> Path:
        """Generate and save a bar chart."""
        labels = specification.data.get("labels")
        values = specification.data.get("values")

        if labels is None or values is None:
            raise ValueError("Bar chart data must contain 'labels' and 'values'.")

        figure, axis = plt.subplots(figsize=(7, 5))
        axis.bar(labels, values)

        axis.set_title(specification.title)
        axis.set_ylabel("Value")
        axis.grid(axis="y", alpha=0.3)

        figure.tight_layout()
        figure.savefig(output_path, dpi=160, bbox_inches="tight")
        plt.close(figure)

        return output_path
