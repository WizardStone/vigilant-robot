# vigilant-robot

A requests-based Python client skeleton for downloading, uploading, and indexing
Scratch projects.

## Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e . -r requirements-dev.txt
pytest
```

## Usage

```python
from vigilant_robot import ScratchClient

with ScratchClient("https://api.example.com", token="your-token") as client:
    project = client.upload_project("project.sb3", metadata={"name": "Demo"})
    archive = client.download_project(project.project_id, "downloaded.sb3")
    index = client.index_projects(limit=25)
```

The default endpoint paths are placeholders. Pass a `paths` mapping to
`ScratchClient` to match the API you are integrating:

```python
client = ScratchClient(
    "https://api.example.com",
    paths={
        "download": "/v1/projects/{project_id}/file",
        "upload": "/v1/projects",
        "index": "/v1/projects/search",
    },
)
```

## Publishing

Create a GitHub release to build and publish the package through the
`Publish to PyPI` workflow. Configure PyPI Trusted Publishing for the
`pypi` GitHub environment before the first release.
