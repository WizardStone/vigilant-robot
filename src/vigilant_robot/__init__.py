"""Client library for working with Scratch projects."""

from .client import ScratchClient
from .exceptions import ScratchAPIError, ScratchHTTPError
from .models import Project, ProjectIndex

__all__ = [
    "Project",
    "ProjectIndex",
    "ScratchAPIError",
    "ScratchClient",
    "ScratchHTTPError",
]

__version__ = "0.1.0"
