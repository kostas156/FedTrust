"""Build human-readable FedTrust assessments from evaluation reports."""

from fedtrust.core.models import EvaluationReport, EvaluationStatus
from fedtrust.reporting.models import AssessmentReport, AssessmentSection, AssessmentSeverity
from fedtrust.reporting.rules import assess_metric


class AssessmentBuilder:
    """Convert evaluation reports into a human-readable assessment."""

    def build(self, reports: list[EvaluationReport]) -> AssessmentReport:
        """Build an assessment report from evaluation results."""
        sections: list[AssessmentSection] = []
        severities: list[AssessmentSeverity] = []

        for report in reports:
            findings = []
            recommendations = []

            for metric in report.metrics:
                finding, recommendation = assess_metric(metric)

                if finding is not None:
                    findings.append(finding)
                    severities.append(finding.severity)

                if recommendation is not None:
                    recommendations.append(recommendation)

            sections.append(
                AssessmentSection(
                    name=report.name,
                    summary=self._build_section_summary(report),
                    findings=findings,
                    recommendations=recommendations,
                    metrics=[
                        {
                            "name": metric.name,
                            "value": metric.value,
                            "unit": metric.unit,
                            "higher_is_better": metric.higher_is_better,
                        }
                        for metric in report.metrics
                    ],
                )
            )

        overall_severity = self._calculate_overall_severity(severities)

        return AssessmentReport(
            title="FedTrust Trustworthiness Assessment",
            executive_summary=self._build_executive_summary(sections, overall_severity),
            overall_severity=overall_severity,
            sections=sections,
        )

    @staticmethod
    def _build_section_summary(report: EvaluationReport) -> str:
        """Build a concise summary for one evaluation section."""
        if report.status is EvaluationStatus.FAILED:
            return f"The {report.name} evaluation failed: {report.error}"

        return f"The {report.name} evaluation completed successfully."

    @staticmethod
    def _build_executive_summary(
        sections: list[AssessmentSection],
        overall_severity: AssessmentSeverity,
    ) -> str:
        """Build the report-level executive summary."""
        findings = [finding for section in sections for finding in section.findings]

        if not findings:
            return (
                "The available evaluations identified no significant findings. "
                "The assessed system currently shows no material issues "
                "under the evaluated criteria."
            )

        highest_priority_findings = [
            finding
            for finding in findings
            if finding.severity
            in {
                AssessmentSeverity.CRITICAL,
                AssessmentSeverity.HIGH,
            }
        ]

        summary = (
            f"Overall assessment: {overall_severity.value.upper()}. "
            f"The evaluation identified {len(findings)} finding"
        )

        if len(findings) != 1:
            summary += "s"

        summary += " requiring attention."

        if highest_priority_findings:
            titles = [finding.title for finding in highest_priority_findings[:2]]

            summary += " The most significant findings are: " + "; ".join(titles) + "."

        return summary

    @staticmethod
    def _calculate_overall_severity(severities: list[AssessmentSeverity]) -> AssessmentSeverity:
        """Return the highest severity among all findings."""
        if not severities:
            return AssessmentSeverity.INFO

        severity_order = {
            AssessmentSeverity.INFO: 0,
            AssessmentSeverity.LOW: 1,
            AssessmentSeverity.MEDIUM: 2,
            AssessmentSeverity.HIGH: 3,
            AssessmentSeverity.CRITICAL: 4,
        }

        return max(severities, key=severity_order.__getitem__)
