from __future__ import annotations

import csv
import io
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _normalize_report_format(report_format: str) -> str:
    normalized = report_format.strip().lower()
    if normalized == "markdown":
        return "md"
    return normalized


def _format_summary_lines(summary: dict[str, Any] | None) -> list[str]:
    if not summary:
        return ["No summary data was provided."]
    lines = []
    for key, value in summary.items():
        if isinstance(value, float):
            lines.append(f"- {key}: {value:.4f}")
        else:
            lines.append(f"- {key}: {value}")
    return lines


def render_markdown_report(*, run_id: str, report_format: str, storage_path: str, summary: dict[str, Any] | None) -> str:
    lines = [
        f"# Evaluation Report",
        "",
        f"- Run ID: {run_id}",
        f"- Format: {report_format}",
        f"- Storage Path: {storage_path}",
        f"- Generated At: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Summary",
        *(_format_summary_lines(summary)),
        "",
    ]
    return "\n".join(lines)


def render_html_report(*, run_id: str, report_format: str, storage_path: str, summary: dict[str, Any] | None) -> str:
    summary_items = "".join(f"<li><strong>{key}</strong>: {value}</li>" for key, value in (summary or {}).items()) or "<li>No summary data was provided.</li>"
    return (
        "<!doctype html>"
        "<html lang=\"en\">"
        "<head><meta charset=\"utf-8\"><title>Evaluation Report</title></head>"
        "<body>"
        "<main>"
        "<h1>Evaluation Report</h1>"
        f"<p><strong>Run ID:</strong> {run_id}</p>"
        f"<p><strong>Format:</strong> {report_format}</p>"
        f"<p><strong>Storage Path:</strong> {storage_path}</p>"
        "<h2>Summary</h2>"
        f"<ul>{summary_items}</ul>"
        "</main>"
        "</body>"
        "</html>"
    )


def render_csv_report(*, run_id: str, report_format: str, storage_path: str, summary: dict[str, Any] | None) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["field", "value"])
    writer.writerow(["run_id", run_id])
    writer.writerow(["report_format", report_format])
    writer.writerow(["storage_path", storage_path])
    for key, value in (summary or {}).items():
        writer.writerow([key, value])
    return buffer.getvalue()


def _pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def render_pdf_report(*, run_id: str, report_format: str, storage_path: str, summary: dict[str, Any] | None) -> bytes:
    lines = [
        "Evaluation Report",
        f"Run ID: {run_id}",
        f"Format: {report_format}",
        f"Storage Path: {storage_path}",
    ]
    for key, value in (summary or {}).items():
        lines.append(f"{key}: {value}")

    content_lines = ["BT", "/F1 12 Tf", "72 760 Td"]
    for index, line in enumerate(lines):
        escaped_line = _pdf_escape(line)
        if index > 0:
            content_lines.append("0 -18 Td")
        content_lines.append(f"({escaped_line}) Tj")
    content_lines.append("ET")
    stream_text = "\n".join(content_lines)
    stream_bytes = stream_text.encode("latin-1", errors="replace")

    objects: list[bytes] = []
    objects.append(b"1 0 obj<< /Type /Catalog /Pages 2 0 R >>endobj\n")
    objects.append(b"2 0 obj<< /Type /Pages /Kids [3 0 R] /Count 1 >>endobj\n")
    objects.append(b"3 0 obj<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>endobj\n")
    objects.append(b"4 0 obj<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>endobj\n")
    objects.append(
        b"5 0 obj<< /Length "
        + str(len(stream_bytes)).encode("ascii")
        + b" >>stream\n"
        + stream_bytes
        + b"\nendstream\nendobj\n"
    )

    output = io.BytesIO()
    output.write(b"%PDF-1.4\n")
    offsets = [0]
    for obj in objects:
        offsets.append(output.tell())
        output.write(obj)
    xref_start = output.tell()
    output.write(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    output.write(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        output.write(f"{offset:010d} 00000 n \n".encode("ascii"))
    output.write(
        (
            "trailer\n"
            f"<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            "startxref\n"
            f"{xref_start}\n"
            "%%EOF"
        ).encode("ascii")
    )
    return output.getvalue()


def render_report_content(*, report_format: str, run_id: str, storage_path: str, summary: dict[str, Any] | None) -> str | bytes:
    normalized = _normalize_report_format(report_format)
    if normalized in {"md", "markdown"}:
        return render_markdown_report(run_id=run_id, report_format=report_format, storage_path=storage_path, summary=summary)
    if normalized == "html":
        return render_html_report(run_id=run_id, report_format=report_format, storage_path=storage_path, summary=summary)
    if normalized == "csv":
        return render_csv_report(run_id=run_id, report_format=report_format, storage_path=storage_path, summary=summary)
    if normalized == "pdf":
        return render_pdf_report(run_id=run_id, report_format=report_format, storage_path=storage_path, summary=summary)
    raise ValueError(f"Unsupported report format: {report_format}")


def resolve_report_path(storage_path: str) -> Path:
    root = Path(__file__).resolve().parents[3]
    relative = Path(storage_path.lstrip("/"))
    resolved = (root / relative).resolve()
    if not resolved.is_relative_to(root):
        raise ValueError(f"Report storage path escapes the repository root: {storage_path}")
    return resolved


def write_report_artifact(*, report_format: str, run_id: str, storage_path: str, summary: dict[str, Any] | None) -> Path:
    output_path = resolve_report_path(storage_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    content = render_report_content(report_format=report_format, run_id=run_id, storage_path=storage_path, summary=summary)
    if isinstance(content, bytes):
        output_path.write_bytes(content)
    else:
        output_path.write_text(content, encoding="utf-8")
    return output_path