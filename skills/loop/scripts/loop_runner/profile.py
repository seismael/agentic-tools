"""Project profile: the single, declarative, project-specific seam.

Everything the loop needs to know about a repository lives in one profile file
(``docs/knowledge/profile.yaml`` by default). The engine is identical for every
project; only this data changes. JSON profile files (or YAML when PyYAML is
installed) are supported so the runner stays dependency-light.
"""

from __future__ import annotations

import dataclasses
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

SCHEMA = "loop.profile.v1"
DEFAULT_PROFILE = "docs/knowledge/profile.yaml"


class ProfileError(ValueError):
    """A missing, unreadable, malformed, or inadmissible profile."""


@dataclass(frozen=True, slots=True)
class Front:
    """One exploration front and its sub-axes."""

    name: str
    required: bool = True
    sub_axes: tuple[str, ...] = ()
    bounded_reason: str = ""


@dataclass(frozen=True, slots=True)
class Stage:
    """One canonical pipeline stage."""

    id: str
    kind: str = "evaluate"
    command: str = ""
    artifact: str = ""
    gate: str = ""


@dataclass(frozen=True, slots=True)
class Profile:
    """Normalized, validated project profile."""

    project: str
    goal: str
    metric: str
    schema: str = SCHEMA
    target: str | None = None
    modes: tuple[str, ...] = ("eval",)
    loop_root: str = ""
    coverage_path: str = "docs/knowledge/coverage.json"
    knowledge_dir: str = "docs/knowledge"
    boundaries: tuple[str, ...] = ()
    fronts: dict[str, Front] = field(default_factory=dict)
    pipeline: tuple[Stage, ...] = ()
    gates: dict[str, str] = field(default_factory=dict)
    completion: dict[str, Any] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)
    path: Path | None = None

    def required_fronts(self) -> dict[str, Front]:
        return {name: front for name, front in self.fronts.items() if front.required}

    def coverage_file(self, project_root: Path) -> Path:
        return (project_root / self.coverage_path).resolve()

    def loop_dir(self, project_root: Path, loop_id: str) -> Path:
        if not self.loop_root:
            raise ProfileError("profile has no paths.loop (journal root)")
        return (project_root / self.loop_root / loop_id).resolve()


def _as_str(value: Any) -> str:
    return "" if value is None else str(value).strip()


def _as_str_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return [_as_str(item) for item in value if _as_str(item)]
    return [_as_str(value)] if _as_str(value) else []


def _parse_fronts(value: Any) -> tuple[dict[str, Front], list[str]]:
    errors: list[str] = []
    fronts: dict[str, Front] = {}
    if not isinstance(value, Mapping) or not value:
        errors.append("fronts must be a non-empty mapping")
        return fronts, errors
    for name, raw in value.items():
        key = _as_str(name)
        if not key:
            errors.append("front name must be a non-empty string")
            continue
        spec = raw if isinstance(raw, Mapping) else {}
        axes = _as_str_list(spec.get("sub_axes"))
        if len(set(axes)) != len(axes):
            errors.append(f"front '{key}' has duplicate sub_axes")
        required = spec.get("required", True)
        if not isinstance(required, bool):
            errors.append(f"front '{key}' required must be a boolean")
            required = True
        fronts[key] = Front(
            name=key,
            required=required,
            sub_axes=tuple(axes),
            bounded_reason=_as_str(spec.get("bounded_reason")),
        )
    return fronts, errors


def _parse_pipeline(value: Any) -> tuple[tuple[Stage, ...], list[str]]:
    errors: list[str] = []
    stages: list[Stage] = []
    if value is None:
        return (), errors
    if not isinstance(value, (list, tuple)):
        errors.append("pipeline must be a list of stages")
        return (), errors
    seen: set[str] = set()
    for raw in value:
        if not isinstance(raw, Mapping):
            errors.append("each pipeline stage must be a mapping")
            continue
        stage_id = _as_str(raw.get("id"))
        if not stage_id:
            errors.append("pipeline stage requires a non-empty id")
            continue
        if stage_id in seen:
            errors.append(f"pipeline stage id '{stage_id}' is duplicated")
        seen.add(stage_id)
        stages.append(
            Stage(
                id=stage_id,
                kind=_as_str(raw.get("kind")) or "evaluate",
                command=_as_str(raw.get("command")),
                artifact=_as_str(raw.get("artifact")),
                gate=_as_str(raw.get("gate")),
            )
        )
    return tuple(stages), errors


def normalize(mapping: Mapping[str, Any]) -> Profile:
    """Build a :class:`Profile` from a raw mapping (no validation-raising)."""
    fronts, _ = _parse_fronts(mapping.get("fronts"))
    pipeline, _ = _parse_pipeline(mapping.get("pipeline"))
    raw_paths = mapping.get("paths")
    paths: Mapping[str, Any] = raw_paths if isinstance(raw_paths, Mapping) else {}
    completion = mapping.get("completion")
    gates = mapping.get("gates")
    return Profile(
        project=_as_str(mapping.get("project")),
        goal=_as_str(mapping.get("goal")),
        metric=_as_str(mapping.get("metric")),
        schema=_as_str(mapping.get("schema")) or SCHEMA,
        target=(_as_str(mapping.get("target")) or None),
        modes=tuple(_as_str_list(mapping.get("modes"))) or ("eval",),
        loop_root=_as_str(paths.get("loop")),
        coverage_path=_as_str(paths.get("coverage")) or "docs/knowledge/coverage.json",
        knowledge_dir=_as_str(paths.get("knowledge")) or "docs/knowledge",
        boundaries=tuple(_as_str_list(mapping.get("boundaries"))),
        fronts=fronts,
        pipeline=pipeline,
        gates={_as_str(k): _as_str(v) for k, v in gates.items()}
        if isinstance(gates, Mapping)
        else {},
        completion=dict(completion) if isinstance(completion, Mapping) else {},
        raw=dict(mapping),
    )


def validate_profile(mapping: Mapping[str, Any]) -> list[str]:
    """Return a list of human-readable validation errors (empty if valid)."""
    errors: list[str] = []
    if not isinstance(mapping, Mapping):
        return ["profile must be a mapping"]

    schema = _as_str(mapping.get("schema"))
    if schema != SCHEMA:
        errors.append(f"schema must be '{SCHEMA}' (found {schema or 'none'!r})")
    for field_name in ("project", "goal", "metric"):
        if not _as_str(mapping.get(field_name)):
            errors.append(f"{field_name} must be a non-empty string")
    if not _as_str_list(mapping.get("modes")):
        errors.append("modes must be a non-empty list")
    if not _as_str_list(mapping.get("boundaries")):
        errors.append("boundaries must be a non-empty list")
    paths = mapping.get("paths")
    if not isinstance(paths, Mapping) or not _as_str(paths.get("loop")):
        errors.append("paths.loop (journal root) is required")

    _, front_errors = _parse_fronts(mapping.get("fronts"))
    errors.extend(front_errors)
    _, pipeline_errors = _parse_pipeline(mapping.get("pipeline"))
    errors.extend(pipeline_errors)

    completion = mapping.get("completion")
    if not isinstance(completion, Mapping):
        errors.append("completion must be a mapping")
    return errors


def _read_mapping(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    stripped = text.lstrip()
    if path.suffix.lower() == ".json" or stripped.startswith("{"):
        data = json.loads(text)
    else:
        try:
            import yaml  # type: ignore
        except ImportError as exc:  # pragma: no cover - depends on environment
            raise ProfileError(
                f"PyYAML is required to load YAML profile {path}; install pyyaml or use JSON syntax"
            ) from exc
        data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ProfileError(f"profile {path} must be a mapping at the top level")
    return data


def load_profile(path: Path | str) -> Profile:
    """Load, normalize, and validate a profile; raise :class:`ProfileError`."""
    path = Path(path)
    if not path.is_file():
        raise ProfileError(f"profile not found: {path}")
    try:
        data = _read_mapping(path)
    except ProfileError:
        raise
    except (OSError, ValueError) as exc:
        raise ProfileError(f"could not parse profile {path}: {exc}") from exc
    errors = validate_profile(data)
    if errors:
        raise ProfileError("; ".join(errors))
    return dataclasses.replace(normalize(data), path=path)


__all__ = [
    "DEFAULT_PROFILE",
    "Front",
    "Profile",
    "ProfileError",
    "SCHEMA",
    "Stage",
    "load_profile",
    "normalize",
    "validate_profile",
]
