"""Chart specifications for FedTrust assessment reports."""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class ChartType(StrEnum):
    """Supported chart types for FedTrust reports."""

    BAR = "bar"
    ROC_CURVE = "roc_curve"


class ChartSpecification(BaseModel):
    """Document-independent specification for a report chart."""

    chart_type: ChartType
    title: str = Field(min_length=1)
    data: dict[str, Any] = Field(default_factory=dict)
    caption: str | None = None
