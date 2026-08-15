# FedTrust

**Open-Source Evaluation Framework for Trustworthy Federated Learning Systems**

FedTrust is an open-source framework for evaluating the **performance, privacy, security, robustness, and overall trustworthiness** of Federated Learning systems through a common, reproducible evaluation architecture.

The project is currently in **active MVP development**.

> **Current stage:** Core evaluation and assessment pipeline implemented.
> **Next major milestone:** User-facing evaluation commands and professional PDF/DOCX assessment reports.

---

## Why FedTrust?

Federated Learning allows machine-learning models to be trained across distributed data sources without directly centralizing the underlying data.

However, decentralizing training does not automatically make a system trustworthy.

A Federated Learning system can still face:

* privacy leakage,
* membership inference attacks,
* security threats,
* robustness failures,
* performance degradation,
* utility/privacy trade-offs.

FedTrust is designed to provide a **systematic way to evaluate these dimensions using a common framework**.

The goal is not to produce isolated metrics, but to transform evaluation evidence into:

**Measurements → Findings → Risk Assessment → Recommendations → Professional Reports**

---

## What FedTrust Does

FedTrust provides a common architecture for executing different evaluations against ML/FL systems.

The current implementation already supports:

### Performance Evaluation

The current MVP includes a classification evaluator that can measure model accuracy from ground-truth labels and predictions.

**Current metric:**

* Accuracy

### Privacy Evaluation

The current MVP includes a Membership Inference Attack evaluation component.

It evaluates attack scores against member/non-member labels and calculates:

* Membership Inference ROC-AUC

The evaluator also validates the evaluation input to prevent invalid privacy results, including:

* mismatched labels and scores,
* empty evaluation data,
* missing member/non-member classes.

### Assessment Layer

Raw evaluation results can be transformed into human-readable assessment findings.

For example:

```text
MIA AUC = 0.72
        ↓
Significant membership leakage
        ↓
Severity: HIGH
        ↓
Recommendation:
Evaluate privacy-preserving training
```

The assessment layer currently supports:

* findings,
* severity levels,
* recommendations,
* section-level summaries,
* overall assessment severity,
* executive summaries.

### Visual Evidence

The reporting layer currently supports chart specifications and chart generation.

Current chart types:

* ROC curves
* Bar charts

Charts are designed as **embedded visual evidence for future PDF/DOCX reports**, not as final user-facing standalone artifacts.

---

# Current Architecture

FedTrust is intentionally organized into separate layers.

```text
                    FedTrust
                        │
                        ▼
               Evaluation Context
                        │
                        ▼
                  Evaluator
                        │
                        ▼
               Evaluation Runner
                        │
                        ▼
              Evaluation Report
                        │
                        ▼
              Assessment Builder
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
         Findings            Recommendations
             │                     │
             └──────────┬──────────┘
                        ▼
                Assessment Report
                        │
                        ▼
                 Visual Evidence
                        │
                        ▼
              DOCX / PDF Reports
```

The architecture follows a deliberate separation of concerns:

### Evaluators

Evaluators answer specific technical questions.

Examples:

```text
How accurate is the model?
Can membership be inferred?
Is the system robust?
Does the system satisfy a privacy requirement?
```

### Evaluation Runner

The runner is responsible for the execution lifecycle.

It handles:

* evaluator execution,
* execution timing,
* structured failure reporting.

It does **not** contain evaluation-specific business logic.

### Evaluation Reports

Evaluators produce a common structured output:

```text
EvaluationReport
├── status
├── metrics
├── duration
├── metadata
└── error
```

This creates a consistent interface across different evaluation methods.

### Assessment Layer

The assessment layer converts technical evidence into human-readable conclusions.

```text
EvaluationReport
        ↓
Assessment Rules
        ↓
Finding / Recommendation
        ↓
AssessmentReport
```

### Reporting Layer

The reporting layer is intentionally separated from the evaluation logic.

The same assessment should eventually be renderable as:

```text
JSON
CSV
DOCX
PDF
```

without recalculating the underlying evaluation metrics.

---

# Current MVP Status

## Implemented

| Capability                     | Status |
| ------------------------------ | ------ |
| Python package structure       | ✅      |
| CLI package                    | ✅      |
| `fedtrust --help`              | ✅      |
| `fedtrust --version`           | ✅      |
| Core domain models             | ✅      |
| `EvaluationContext`            | ✅      |
| `Evaluator` protocol           | ✅      |
| `EvaluationRunner`             | ✅      |
| Structured `EvaluationReport`  | ✅      |
| Classification evaluator       | ✅      |
| Accuracy metric                | ✅      |
| Membership inference evaluator | ✅      |
| MIA ROC-AUC                    | ✅      |
| MIA input validation           | ✅      |
| Assessment models              | ✅      |
| Assessment rules               | ✅      |
| Findings                       | ✅      |
| Recommendations                | ✅      |
| Overall severity               | ✅      |
| Assessment builder             | ✅      |
| ROC chart generation           | ✅      |
| Bar chart generation           | ✅      |
| Unit tests                     | ✅      |
| Integration tests              | ✅      |
| Ruff / pre-commit              | ✅      |
| mypy                           | ✅      |

### Current test status

**32 automated tests passing**

The project currently validates:

* package behavior,
* CLI behavior,
* core evaluation models,
* evaluator contracts,
* evaluation execution,
* classification evaluation,
* membership inference evaluation,
* assessment generation,
* chart generation.

---

# In Progress

The following capabilities are the next major MVP milestones:

### User-facing evaluation CLI

Planned commands include:

```bash
fedtrust run
fedtrust compare
```

The goal is to allow users to run evaluations without writing Python code for every experiment.

### Professional assessment reports

The next reporting milestone is:

```text
FedTrust Assessment
        │
        ├── Executive Summary
        ├── Findings
        ├── Recommendations
        ├── Metrics
        ├── Charts
        └── Technical Appendix
              │
              ├── DOCX
              └── PDF
```

The final reports should contain the charts and findings **inside the document itself**, rather than exposing users to separate image files.

### Evaluation registry

Evaluators will be discoverable through a common registry so that commands such as:

```bash
fedtrust run --evaluation classification
fedtrust run --evaluation membership_inference
```

can map evaluation names to concrete implementations.

---

# Planned Trustworthiness Dimensions

The long-term FedTrust evaluation model is broader than the currently implemented MVP.

```text
                  Trustworthiness
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
   Performance         Privacy          Security
        │                │                │
    Accuracy            MIA           Attack tests
    F1 / etc.           DP            Threat checks
        │                │                │
        └────────────────┼────────────────┘
                         ▼
                    Robustness
                         │
                  Stress / attacks
```

Planned evaluation areas include:

* Differential Privacy
* Robustness
* Security
* Privacy–utility trade-offs
* Model comparison
* Additional trustworthiness metrics

These components will be added without changing the existing evaluator/runner/reporting contracts whenever possible.

---

# Research Direction

FedTrust is designed with both **engineering and research use cases** in mind.

A key research direction is the evaluation of trade-offs between:

```text
Model Utility
       ↕
Privacy Protection
       ↕
Security / Robustness
```

For example, a model should not be considered trustworthy simply because its privacy leakage is low if achieving that result causes unacceptable utility degradation.

FedTrust therefore aims to make these trade-offs measurable and comparable through standardized evaluation results and assessment reports.

---

# Example Evaluation Flow

A future end-to-end workflow is expected to look like:

```text
1. Select model and dataset
2. Configure evaluations
3. Run evaluation pipeline
4. Collect structured metrics
5. Interpret results
6. Generate findings and recommendations
7. Generate professional assessment report
```

Conceptually:

```text
Model + Dataset
      │
      ▼
Evaluation Configuration
      │
      ▼
Evaluation Engine
      │
      ├── Classification
      ├── Membership Inference
      ├── Differential Privacy
      ├── Robustness
      └── Security
      │
      ▼
Evaluation Reports
      │
      ▼
Assessment Builder
      │
      ▼
Findings + Recommendations
      │
      ▼
Professional Report
```

---

# Development Philosophy

FedTrust follows several principles:

### Separation of Concerns

Evaluation logic, execution, assessment and presentation remain separate.

```text
Evaluator ≠ Runner ≠ Assessment ≠ Renderer
```

### Reproducibility

Evaluation outputs should be structured, traceable and suitable for comparison across experiments.

### Explicit Failure Handling

Invalid evaluation inputs should produce structured failures instead of silently producing misleading metrics.

### Technology-Agnostic Core

The core evaluation architecture should remain independent from specific ML/FL frameworks where possible.

Technology-specific integrations can be added at the edges.

### Test-Driven Validation

New functionality should be backed by automated tests before becoming part of the stable project baseline.

---

# Project Structure

```text
FedTrust/
├── src/
│   └── fedtrust/
│       ├── cli/
│       ├── core/
│       │   ├── models.py
│       │   ├── protocols.py
│       │   └── runner.py
│       ├── evaluation/
│       │   └── classification.py
│       ├── privacy/
│       │   └── membership_inference.py
│       ├── reporting/
│       │   ├── models.py
│       │   ├── rules.py
│       │   ├── builder.py
│       │   ├── charts.py
│       │   └── chart_generator.py
│       ├── fl/
│       ├── governance/
│       ├── security/
│       └── utils/
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── docs/
├── examples/
├── experiments/
├── reports/
├── scripts/
├── pyproject.toml
├── README.md
├── LICENSE
└── NOTICE
```

Some planned modules currently contain only project scaffolding and will be implemented as the corresponding MVP capabilities are introduced.

---

# Installation

FedTrust currently targets Python 3.11+.

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/kostas156/FedTrust.git
cd FedTrust

python -m venv .venv
```

Activate the environment and install the development dependencies:

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

### Linux / macOS

```bash
source .venv/bin/activate
pip install -e ".[dev]"
```

---

# Current CLI

The initial CLI is available:

```bash
fedtrust --help
fedtrust --version
```

Current version:

```text
0.1.0
```

The main evaluation commands are under active development.

---

# Quality & Validation

The project currently uses:

* **pytest** for automated testing
* **mypy** for static type checking
* **Ruff** for linting and formatting
* **pre-commit** for automated quality checks

Current baseline:

```text
32 tests passing
mypy: clean
ruff: clean
```

The repository uses automated validation to help prevent invalid evaluation results and regressions in the core architecture.

---

# Roadmap

## Phase 1 — Foundation

* [x] Repository structure
* [x] Packaging
* [x] CLI skeleton
* [x] Core evaluation architecture
* [x] Evaluation runner
* [x] Structured evaluation reports

## Phase 2 — Initial Evaluations

* [x] Classification evaluation
* [x] Membership inference evaluation
* [x] Assessment rules
* [x] Findings and recommendations
* [x] Chart generation

## Phase 3 — MVP Productization

* [ ] Evaluation registry
* [ ] `fedtrust run`
* [ ] `fedtrust compare`
* [ ] Configuration-based evaluations
* [ ] Professional DOCX report generation
* [ ] Professional PDF report generation
* [ ] Embedded charts in reports
* [ ] Reproducible assessment metadata

## Phase 4 — Trustworthiness Expansion

* [ ] Differential Privacy evaluation
* [ ] Robustness evaluation
* [ ] Security evaluation
* [ ] Privacy–utility analysis
* [ ] Expanded attack suite
* [ ] Advanced comparison engine

## Phase 5 — Future

* [ ] Web dashboard
* [ ] Interactive visualization
* [ ] Advanced trustworthiness scoring
* [ ] Experiment management
* [ ] Larger-scale FL integrations

---

# Project Status

**Development stage: Active MVP development**

FedTrust is currently beyond the initial repository/scaffolding stage and already contains a working evaluation and assessment pipeline.

However, it should **not yet be considered a finished production platform**.

The current project is best described as:

> **A working open-source prototype of a trustworthiness evaluation and assessment framework for Federated Learning systems.**

The next milestone is to turn the current evaluation engine into a complete user-facing MVP through:

**CLI execution + professional PDF/DOCX reports + additional trustworthiness evaluations.**

---

# Contributing

FedTrust is being developed as an open-source project.

Contributions should preserve the core design principles:

* clear separation of concerns,
* typed interfaces,
* reproducible evaluation behavior,
* explicit failure handling,
* automated tests,
* maintainable documentation.

Before submitting changes, run:

```bash
python -m pytest
python -m mypy src
python -m pre_commit run --all-files
```

---

# License

FedTrust is released under the **Apache License 2.0**.

See [`LICENSE`](LICENSE) for the complete license text and [`NOTICE`](NOTICE) for attribution and third-party notices.

---

# Project Vision

FedTrust aims to become an open evaluation layer for Federated Learning systems that answers a broader question than:

> **"Does the model work?"**

The long-term goal is to answer:

> **"How trustworthy is this Federated Learning system, under measurable performance, privacy, security and robustness criteria?"**

The intended output is not simply a collection of metrics.

It is a reproducible chain of evidence:

```text
Experiment
   ↓
Evaluation
   ↓
Evidence
   ↓
Assessment
   ↓
Findings
   ↓
Recommendations
   ↓
Professional Report
```

That is the core vision behind FedTrust.

---

**FedTrust** — Open-Source Evaluation Framework for Trustworthy Federated Learning Systems

Repository: `https://github.com/kostas156/FedTrust`

License: **Apache-2.0**
