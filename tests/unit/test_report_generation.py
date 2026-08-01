from pathlib import Path

from app.reports.generator import render_report_content, write_report_artifact


def test_render_report_content_supports_all_formats() -> None:
    summary = {"pass_rate": 0.95, "failure_count": 3}

    markdown = render_report_content(
        report_format="markdown",
        run_id="run-1",
        storage_path="/reports/run-1.md",
        summary=summary,
    )
    html = render_report_content(
        report_format="html",
        run_id="run-1",
        storage_path="/reports/run-1.html",
        summary=summary,
    )
    csv_report = render_report_content(
        report_format="csv",
        run_id="run-1",
        storage_path="/reports/run-1.csv",
        summary=summary,
    )
    pdf = render_report_content(
        report_format="pdf",
        run_id="run-1",
        storage_path="/reports/run-1.pdf",
        summary=summary,
    )

    assert isinstance(markdown, str)
    assert "# Evaluation Report" in markdown
    assert isinstance(html, str)
    assert "<html" in html
    assert isinstance(csv_report, str)
    assert "pass_rate" in csv_report
    assert isinstance(pdf, bytes)
    assert pdf.startswith(b"%PDF-1.4")


def test_write_report_artifact_writes_to_resolved_location(tmp_path, monkeypatch) -> None:
    target = tmp_path / "generated" / "report.md"

    monkeypatch.setattr("app.reports.generator.resolve_report_path", lambda storage_path: target)

    written_path = write_report_artifact(
        report_format="markdown",
        run_id="run-1",
        storage_path="/reports/run-1.md",
        summary={"pass_rate": 0.91},
    )

    assert written_path == target
    assert target.exists()
    assert "Evaluation Report" in target.read_text(encoding="utf-8")