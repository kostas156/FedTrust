"""Core protocols for FedTrust evaluations."""

from typing import Protocol, runtime_checkable

from fedtrust.core.models import EvaluationContext, EvaluationReport


@runtime_checkable
class Evaluator(Protocol):
    """Protocol implemented by concrete FedTrust evaluators."""

    @property
    def name(self) -> str:
        """Return the name of the evaluator."""

    def evaluate(self, context: EvaluationContext) -> EvaluationReport:
        """Run the evaluation and return a structured report."""
