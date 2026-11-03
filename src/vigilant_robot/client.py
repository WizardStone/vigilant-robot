"""HTTP client for a Scratch-project API."""

from collections.abc import Mapping
from pathlib import Path
from typing import Any, Optional, Union

import requests

from .exceptions import ScratchHTTPError
from .models import Project, ProjectIndex


class ScratchClient:
    """A small requests-based client with overridable API paths.

    The default paths are placeholders for the target API. Override ``paths`` when
    connecting to an API with different routes.
    """

    DEFAULT_PATHS = {
        "download": "/projects/{project_id}/download",
        "upload": "/projects",
        "index": "/projects",
    }

    def __init__(
        self,
        base_url: str,
        *,
        token: Optional[str] = None,
        session: Optional[requests.Session] = None,
        timeout: float = 30.0,
        paths: Optional[Mapping[str, str]] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = session or requests.Session()
        self.paths = {**self.DEFAULT_PATHS, **(paths or {})}
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})
        self.session.headers.setdefault("Accept", "application/json")

    def download_project(
        self, project_id: str, destination: Optional[Union[str, Path]] = None
    ) -> bytes:
        """Download a project archive, optionally writing it to ``destination``."""
        response = self._request("GET", self.paths["download"].format(project_id=project_id))
        content = response.content
        if destination is not None:
            Path(destination).write_bytes(content)
        return content

    def upload_project(
        self,
        project: Union[bytes, bytearray, str, Path],
        *,
        filename: Optional[str] = None,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> Project:
        """Upload project bytes or a file path and return the API project."""
        if isinstance(project, (str, Path)):
            path = Path(project)
            payload = path.read_bytes()
            filename = filename or path.name
        else:
            payload = bytes(project)
            filename = filename or "project.sb3"
        response = self._request(
            "POST",
            self.paths["upload"],
            files={"project": (filename, payload, "application/octet-stream")},
            data=dict(metadata or {}),
        )
        return Project.from_dict(response.json())

    def index_projects(self, **params: Any) -> ProjectIndex:
        """Return an index page; pagination/filter parameters are passed through."""
        response = self._request("GET", self.paths["index"], params=params)
        return ProjectIndex.from_dict(response.json())

    def close(self) -> None:
        """Close the underlying requests session."""
        self.session.close()

    def __enter__(self) -> "ScratchClient":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        url = f"{self.base_url}/{path.lstrip('/')}"
        response = self.session.request(method, url, timeout=self.timeout, **kwargs)
        if not response.ok:
            try:
                message = response.json().get("message", response.text)
            except ValueError:
                message = response.text
            raise ScratchHTTPError(response.status_code, str(message), response.url)
        return response
