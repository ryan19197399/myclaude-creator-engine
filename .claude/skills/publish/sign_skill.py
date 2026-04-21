"""sign_skill.py — Cryptographic signing for skill packages.

Generates a SHA-256 content hash and writes a .signature file
next to SKILL.md so downstream consumers can verify integrity.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional


@dataclass
class SignatureResult:
    success: bool
    skill_path: Path
    signature_file: Optional[Path] = None
    content_hash: Optional[str] = None
    signed_files: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def __str__(self) -> str:
        if self.success:
            return (
                f"✅ Signed {self.skill_path.name} "
                f"(sha256:{self.content_hash[:12]}…)"
            )
        return f"❌ Sign failed for {self.skill_path}: {'; '.join(self.errors)}"


# Files that are included in the content hash (order matters).
_SIGNABLE_FILES = [
    "SKILL.md",
    "README.md",
    "CHANGELOG.md",
    "LICENSE.md",
]


def _hash_file(path: Path) -> str:
    """Return the hex SHA-256 digest of a single file."""
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65_536), b""):
            h.update(chunk)
    return h.hexdigest()


def _collect_python_files(skill_dir: Path) -> List[Path]:
    """Return sorted .py files found directly inside the skill directory."""
    return sorted(skill_dir.glob("*.py"))


def compute_skill_hash(skill_dir: Path) -> tuple[str, List[str]]:
    """Compute a deterministic hash over all signable artefacts.

    Returns (hex_digest, list_of_relative_paths_included).
    """
    h = hashlib.sha256()
    included: List[str] = []

    # 1. Well-known docs (present or absent — absence is skipped silently).
    for name in _SIGNABLE_FILES:
        candidate = skill_dir / name
        if candidate.exists():
            h.update(name.encode())
            h.update(_hash_file(candidate).encode())
            included.append(name)

    # 2. Any Python helpers bundled with the skill.
    for py_path in _collect_python_files(skill_dir):
        rel = py_path.name
        h.update(rel.encode())
        h.update(_hash_file(py_path).encode())
        included.append(rel)

    return h.hexdigest(), included


def sign_skill(skill_dir: Path | str) -> SignatureResult:
    """Create or overwrite a `.signature` file for the given skill directory.

    The signature file is a JSON document containing:
    - ``content_hash``: SHA-256 over all signable files.
    - ``signed_files``: ordered list of files that were hashed.
    - ``signed_at``: ISO-8601 UTC timestamp.
    - ``tool``: constant identifier for this signing tool.

    Args:
        skill_dir: Path to the skill directory (must contain at least SKILL.md).

    Returns:
        :class:`SignatureResult` describing the outcome.
    """
    skill_dir = Path(skill_dir)
    result = SignatureResult(success=False, skill_path=skill_dir)

    if not skill_dir.is_dir():
        result.errors.append(f"Not a directory: {skill_dir}")
        return result

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        result.errors.append("SKILL.md not found — cannot sign an incomplete skill")
        return result

    try:
        content_hash, signed_files = compute_skill_hash(skill_dir)
    except OSError as exc:
        result.errors.append(f"I/O error while hashing: {exc}")
        return result

    payload = {
        "tool": "myclaude-creator-engine/publish",
        "content_hash": content_hash,
        "signed_files": signed_files,
        "signed_at": datetime.now(timezone.utc).isoformat(),
    }

    sig_path = skill_dir / ".signature"
    try:
        sig_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    except OSError as exc:
        result.errors.append(f"Could not write {sig_path}: {exc}")
        return result

    result.success = True
    result.signature_file = sig_path
    result.content_hash = content_hash
    result.signed_files = signed_files
    return result


if __name__ == "__main__":  # pragma: no cover
    import sys

    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    outcome = sign_skill(target)
    print(outcome)
    sys.exit(0 if outcome.success else 1)
