from pathlib import Path

from evals import runner


def test_scan_debug_reports_relative_file(tmp_path):
    code_file = tmp_path / "app.py"
    code_file.write_text("print('debug')\n", encoding="utf-8")

    hits = runner.scan_debug(tmp_path)

    assert hits == [{"file": "app.py", "line": 1, "match": "print('debug')"}]


def test_scan_blacklist_ignores_workflow_examples_in_history():
    repo = Path(__file__).resolve().parents[1]

    hits = runner.scan_blacklist_tools(repo)

    assert not [
        hit for hit in hits
        if hit.get("type") == "ci_workflow_modified"
        and hit.get("file", "").endswith(".yml.example")
    ]
