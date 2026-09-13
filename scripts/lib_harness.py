#!/usr/bin/env python3
"""Shared helpers for ai-harness-kit maintenance scripts."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / ".ai" / "skills-manifest.json"


def load_manifest(path: Path = MANIFEST_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def skill_repo(skill: dict[str, str], protocol: str) -> str:
    key = "repo_https" if protocol == "https" else "repo_ssh"
    return skill[key]


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def current_branch(repo: Path) -> str:
    result = run(["git", "branch", "--show-current"], cwd=repo)
    return result.stdout.strip() if result.returncode == 0 else ""
