from pathlib import Path

import requests

from vigilant_robot import Project, ScratchClient


def test_download_project_writes_archive(tmp_path: Path) -> None:
    session = requests.Session()
    client = ScratchClient("https://example.test", session=session)
    response = requests.Response()
    response.status_code = 200
    response._content = b"sb3-data"
    response.url = "https://example.test/projects/42/download"
    session.request = lambda *args, **kwargs: response  # type: ignore[method-assign]

    destination = tmp_path / "project.sb3"
    assert client.download_project("42", destination) == b"sb3-data"
    assert destination.read_bytes() == b"sb3-data"


def test_upload_project_returns_model() -> None:
    session = requests.Session()
    client = ScratchClient("https://example.test", session=session)
    response = requests.Response()
    response.status_code = 201
    response._content = b'{"id": "42", "name": "Demo"}'
    response.url = "https://example.test/projects"
    session.request = lambda *args, **kwargs: response  # type: ignore[method-assign]

    result = client.upload_project(b"project")
    assert isinstance(result, Project)
    assert result.project_id == "42"
    assert result.name == "Demo"
