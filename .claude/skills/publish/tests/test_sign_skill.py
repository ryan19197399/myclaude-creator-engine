"""Tests for sign_skill.py — skill directory hashing and signature generation."""

import hashlib
import json
from pathlib import Path

import pytest

from sign_skill import (
    SignatureResult,
    _collect_python_files,
    _hash_file,
    compute_skill_hash,
    sign_skill,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def skill_dir(tmp_path: Path) -> Path:
    """Minimal skill directory with the files sign_skill cares about."""
    # Required markdown files
    (tmp_path / "SKILL.md").write_text("# My Skill\nversion: 1.0.0\n")
    (tmp_path / "README.md").write_text("# README\n")
    (tmp_path / "CHANGELOG.md").write_text("## 1.0.0\n- Initial release\n")

    # A couple of Python source files
    (tmp_path / "main.py").write_text("def run(): pass\n")
    sub = tmp_path / "helpers"
    sub.mkdir()
    (sub / "utils.py").write_text("def helper(): return 42\n")

    return tmp_path


# ---------------------------------------------------------------------------
# _hash_file
# ---------------------------------------------------------------------------


class TestHashFile:
    def test_deterministic(self, tmp_path: Path) -> None:
        f = tmp_path / "sample.txt"
        f.write_text("hello world")
        assert _hash_file(f) == _hash_file(f)

    def test_known_hash(self, tmp_path: Path) -> None:
        f = tmp_path / "known.txt"
        content = b"hello world"
        f.write_bytes(content)
        expected = hashlib.sha256(content).hexdigest()
        assert _hash_file(f) == expected

    def test_different_content_different_hash(self, tmp_path: Path) -> None:
        f1 = tmp_path / "a.txt"
        f2 = tmp_path / "b.txt"
        f1.write_text("foo")
        f2.write_text("bar")
        assert _hash_file(f1) != _hash_file(f2)


# ---------------------------------------------------------------------------
# _collect_python_files
# ---------------------------------------------------------------------------


class TestCollectPythonFiles:
    def test_finds_all_py_files(self, skill_dir: Path) -> None:
        files = _collect_python_files(skill_dir)
        names = {f.name for f in files}
        assert "main.py" in names
        assert "utils.py" in names

    def test_excludes_non_py(self, skill_dir: Path) -> None:
        files = _collect_python_files(skill_dir)
        for f in files:
            assert f.suffix == ".py"

    def test_excludes_test_files(self, skill_dir: Path) -> None:
        tests_dir = skill_dir / "tests"
        tests_dir.mkdir()
        (tests_dir / "test_main.py").write_text("def test_x(): pass\n")
        files = _collect_python_files(skill_dir)
        for f in files:
            assert "tests" not in f.parts

    def test_returns_sorted(self, skill_dir: Path) -> None:
        files = _collect_python_files(skill_dir)
        paths = [str(f) for f in files]
        assert paths == sorted(paths)

    def test_empty_dir(self, tmp_path: Path) -> None:
        assert _collect_python_files(tmp_path) == []


# ---------------------------------------------------------------------------
# compute_skill_hash
# ---------------------------------------------------------------------------


class TestComputeSkillHash:
    def test_returns_hex_string(self, skill_dir: Path) -> None:
        digest = compute_skill_hash(skill_dir)
        assert isinstance(digest, str)
        assert len(digest) == 64  # SHA-256 hex

    def test_deterministic(self, skill_dir: Path) -> None:
        assert compute_skill_hash(skill_dir) == compute_skill_hash(skill_dir)

    def test_changes_on_content_modification(self, skill_dir: Path) -> None:
        before = compute_skill_hash(skill_dir)
        (skill_dir / "main.py").write_text("def run(): return 99\n")
        after = compute_skill_hash(skill_dir)
        assert before != after

    def test_changes_on_new_file(self, skill_dir: Path) -> None:
        before = compute_skill_hash(skill_dir)
        (skill_dir / "extra.py").write_text("x = 1\n")
        after = compute_skill_hash(skill_dir)
        assert before != after


# ---------------------------------------------------------------------------
# sign_skill / SignatureResult
# ---------------------------------------------------------------------------


class TestSignSkill:
    def test_success(self, skill_dir: Path) -> None:
        result = sign_skill(skill_dir)
        assert result.success is True
        assert result.skill_hash
        assert result.signature_file is not None
        assert result.signature_file.exists()

    def test_signature_file_is_valid_json(self, skill_dir: Path) -> None:
        result = sign_skill(skill_dir)
        data = json.loads(result.signature_file.read_text())
        assert "skill_hash" in data
        assert "signed_at" in data
        assert "files" in data

    def test_hash_in_file_matches_result(self, skill_dir: Path) -> None:
        result = sign_skill(skill_dir)
        data = json.loads(result.signature_file.read_text())
        assert data["skill_hash"] == result.skill_hash

    def test_missing_skill_md(self, tmp_path: Path) -> None:
        # No SKILL.md — should fail gracefully
        result = sign_skill(tmp_path)
        assert result.success is False
        assert result.error

    def test_str_representation(self, skill_dir: Path) -> None:
        result = sign_skill(skill_dir)
        text = str(result)
        assert "skill_hash" in text or result.skill_hash[:8] in text
