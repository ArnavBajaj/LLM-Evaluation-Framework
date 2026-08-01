# Requirements

## Functional Requirements

- Evaluate multiple LLM providers behind a common interface.
- Run large prompt suites in parallel with retries and rate limits.
- Persist every run, prompt version, dataset version, response, score, and trace.
- Detect hallucination, bias, toxicity, prompt injection, jailbreaks, reasoning failures, and formatting violations.
- Compare model versions side by side and surface regressions.
- Export reports in HTML, Markdown, PDF, and CSV.
- Support login and role-based access control.

## Non-Functional Requirements

- Reproducible runs with immutable versioning.
- Deterministic tests with provider mocks.
- Clear OpenAPI documentation.
- Production-oriented observability and auditability.
- Containerized local development with Docker Compose.
- Designed to support CI/CD regression checks.

## Out of Scope for Initial Build

- Fine-tuning pipelines.
- Public multi-tenant SaaS billing.
- Agentic autonomous browsing systems.
- Kubernetes deployment before the first working MVP.