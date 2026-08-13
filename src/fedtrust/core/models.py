"""Core domain models for FedTrust evaluations."""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class EvaluationStatus(StrEnum):
    """Lifecycle status of an evaluation."""

    SUCCESS = "success"
    FAILED = "failed"


class MetricResult(BaseModel):
    """Result of a single evaluation metric."""

    name: str = Field(min_length=1)
    value: float
    unit: str | None = None
    higher_is_better: bool | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class EvaluationReport(BaseModel):
    """Structured output produced by a FedTrust evaluation."""

    name: str = Field(min_length=1)
    status: EvaluationStatus
    metrics: list[MetricResult] = Field(default_factory=list)
    duration_seconds: float | None = Field(default=None, ge=0)
    metadata: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None


class EvaluationContext(BaseModel):
    """Input context provided to a FedTrust evaluator."""

    model_name: str = Field(min_length=1)
    dataset_name: str = Field(min_length=1)
    model_metadata: dict[str, Any] = Field(default_factory=dict)
    dataset_metadata: dict[str, Any] = Field(default_factory=dict)
    evaluation_metadata: dict[str, Any] = Field(default_factory=dict)
