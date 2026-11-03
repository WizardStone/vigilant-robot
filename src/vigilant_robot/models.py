"""Small, intentionally extensible data models for Scratch projects."""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class Project:
    """A Scratch project payload returned by or sent to the API."""

    project_id: Optional[str] = None
    name: Optional[str] = None
    data: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Project":
        project_id = payload.get("id", payload.get("project_id"))
        name = payload.get("name")
        return cls(
            project_id=str(project_id) if project_id is not None else None,
            name=name,
            data=payload,
        )


@dataclass
class ProjectIndex:
    """A page of indexed projects and optional pagination metadata."""

    projects: list[Project] = field(default_factory=list)
    next_cursor: Optional[str] = None
    data: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ProjectIndex":
        raw_projects = payload.get("projects", payload.get("items", []))
        return cls(
            projects=[Project.from_dict(item) for item in raw_projects],
            next_cursor=payload.get("next_cursor", payload.get("next")),
            data=payload,
        )
