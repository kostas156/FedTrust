"""Canonical assessment models for FedTrust reports."""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class AssessmentSeverity(StrEnum):
    """Severity assigned to an assessment finding."""

    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Finding(BaseModel):
    """Human-readable finding derived from evaluation evidence."""

    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    severity: AssessmentSeverity
    evidence: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class Recommendation(BaseModel):
    """Actionable recomendation derived from an assessment finding."""

    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    priority: AssessmentSeverity = AssessmentSeverity.MEDIUM


class AssessmentSection(BaseModel):
    """Logical section of a FedTrust assessment report."""

    name: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    findings: list[Finding] = Field(default_factory=list)
    recommendations: list[Recommendation] = Field(default_factory=list)
    metrics: list[dict[str, Any]] = Field(default_factory=list)


class AssessmentReport(BaseModel):
    """Canonical human-readable FedTrust assessment."""

    title: str = Field(min_length=1)
    executive_summary: str = Field(min_length=1)
    overall_severity: AssessmentSeverity
    sections: list[AssessmentSection] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
