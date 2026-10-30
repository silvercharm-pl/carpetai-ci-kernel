"""Dependency-free, fail-closed classifier with a synthetic example policy."""
from dataclasses import dataclass
from pathlib import PurePosixPath
import re

LEVELS = {"GREEN": 0, "YELLOW": 1, "RED": 2}
_VALID = re.compile(r"^[A-Za-z0-9_.@+/-]+$")


@dataclass(frozen=True)
class Policy:
    green: tuple[str, ...] = ("docs/**",)
    yellow: tuple[str, ...] = ("src/**", "tests/**")
    red: tuple[str, ...] = (".github/**", "security/**")
    max_green_files: int = 20


def _matches(path: str, pattern: str) -> bool:
    # Simple directory-prefix allowlist; no glob interpretation across levels.
    if pattern.endswith("/**"):
        return path.startswith(pattern[:-2]) and len(path) > len(pattern[:-2])
    return path == pattern


def _valid_path(path: object) -> bool:
    return (isinstance(path, str) and bool(path) and
            _VALID.fullmatch(path) is not None and
            not path.startswith(("/", "./")) and
            all(part not in ("", ".", "..") for part in path.split("/")) and
            ":" not in path and
            PurePosixPath(path).as_posix() == path)


def classify(changes: list[dict], policy: Policy = Policy()) -> dict:
    if not isinstance(changes, list) or not changes:
        return {"level": "RED", "reason": "missing_changes"}
    if not isinstance(policy, Policy) or type(policy.max_green_files) is not int or policy.max_green_files < 1:
        return {"level": "RED", "reason": "invalid_policy"}
    for rules in (policy.green, policy.yellow, policy.red):
        if not isinstance(rules, tuple):
            return {"level": "RED", "reason": "invalid_policy"}
        for rule in rules:
            if not isinstance(rule, str) or not rule:
                return {"level": "RED", "reason": "invalid_policy"}
            base = rule[:-3] if rule.endswith("/**") else rule
            if not _valid_path(base):
                return {"level": "RED", "reason": "invalid_policy"}
    if len(changes) > policy.max_green_files:
        return {"level": "RED", "reason": "change_count_exceeded"}
    outcome = "GREEN"
    for change in changes:
        if not isinstance(change, dict):
            return {"level": "RED", "reason": "invalid_change"}
        path, status, patch = change.get("path"), change.get("status"), change.get("patch")
        if not _valid_path(path):
            return {"level": "RED", "reason": "invalid_path"}
        if status not in ("added", "modified") or not isinstance(patch, str) or not patch.strip():
            return {"level": "RED", "reason": "missing_or_unsafe_patch"}
        if any(_matches(path, g) for g in policy.red):
            return {"level": "RED", "reason": "red_path"}
        candidate = ("GREEN" if any(_matches(path, g) for g in policy.green)
                     else "YELLOW" if any(_matches(path, g) for g in policy.yellow)
                     else "RED")
        if LEVELS[candidate] > LEVELS[outcome]:
            outcome = candidate
    return {"level": outcome, "reason": "classified"}
