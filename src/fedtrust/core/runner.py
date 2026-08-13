"""Execution orchestration for the FedTrust evaluations."""

from time import perf_counter

from fedtrust.core.models import EvaluationContext, EvaluationReport, EvaluationStatus
from fedtrust.core.protocols import Evaluator


class EvaluationRunner:
    """Execute evaluators and produce standardized evaluation reports."""

    def run(self, evaluator: Evaluator, context: EvaluationContext) -> EvaluationReport:
        """Run an evaluator and return its evaluation report."""
        start_time = perf_counter()

        try:
            report = evaluator.evaluate(context)
        except Exception as exc:
            duration = perf_counter() - start_time

            return EvaluationReport(
                name=evaluator.name,
                status=EvaluationStatus.FAILED,
                duration_seconds=duration,
                error=str(exc),
            )

        duration = perf_counter() - start_time

        return report.model_copy(update={"duration_seconds": duration})
