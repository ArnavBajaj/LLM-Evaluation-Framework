import json
from pathlib import Path


def test_health_endpoints(api_client) -> None:
    root_response = api_client.get("/healthz")
    api_response = api_client.get("/api/v1/health")

    assert root_response.status_code == 200
    assert root_response.json() == {"status": "ok"}
    assert api_response.status_code == 200
    assert api_response.json() == {"status": "ok"}


def test_catalog_endpoints_return_expected_shapes(api_client) -> None:
    endpoints = ["/api/v1/datasets/", "/api/v1/models/", "/api/v1/prompts/", "/api/v1/runs/", "/api/v1/metrics/", "/api/v1/reports/"]

    for endpoint in endpoints:
        response = api_client.get(endpoint)
        assert response.status_code == 200
        payload = response.json()
        assert isinstance(payload, dict)

    assert len(api_client.get("/api/v1/datasets/").json()["items"]) >= 2
    assert len(api_client.get("/api/v1/models/").json()["items"]) >= 5
    assert len(api_client.get("/api/v1/prompts/").json()["items"]) >= 2
    assert len(api_client.get("/api/v1/runs/").json()["items"]) >= 2
    assert len(api_client.get("/api/v1/reports/").json()["items"]) >= 1


def test_openapi_document_includes_phase_8_and_9_routes(api_client) -> None:
    response = api_client.get("/api/v1/openapi.json")

    assert response.status_code == 200
    spec = response.json()
    expected_paths = {
        "/api/v1/health",
        "/api/v1/datasets/",
        "/api/v1/models/",
        "/api/v1/prompts/",
        "/api/v1/runs/",
        "/api/v1/metrics/",
        "/api/v1/reports/",
    }
    assert expected_paths.issubset(spec["paths"].keys())


def test_api_response_regression_fixture_alignment(api_client) -> None:
    root = Path(__file__).resolve().parents[1]
    prompt_fixture = json.loads((root / "fixtures" / "prompt_template.json").read_text())
    run_fixture = json.loads((root / "fixtures" / "evaluation_run.json").read_text())

    assert prompt_fixture["version"] == "v3"
    assert prompt_fixture["tags"] == ["jailbreak", "policy"]
    assert run_fixture["provider_name"] == "openai"
    assert run_fixture["seed"] == 42
    prompt_items = api_client.get("/api/v1/prompts/").json()["items"]
    seeded_prompt = next(item for item in prompt_items if item["title"] == "Adversarial jailbreak test")
    assert seeded_prompt["version"] == "v3"
    assert seeded_prompt["tags"] == ["jailbreak", "policy"]
