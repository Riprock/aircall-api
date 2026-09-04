"""Guards against unresolved Pydantic forward references.

Models that reference each other (User <-> Number) must declare one side as a
string forward ref. If nothing resolves that ref, the model stays incomplete and
raises "`User` is not fully defined" on the first validation rather than at
import -- which is how 1.2.0 shipped with most read paths broken.

The failure is caller-dependent: Pydantic falls back to the calling frame's
namespace, so a model can validate fine in a scope that happens to hold the
missing type and fail in one that does not. These tests pin down both the
resolved state and the import order that exposes it.
"""

import os
import pathlib
import subprocess
import sys

import pytest

import aircall.models as models

# Directory holding the `aircall` package, for subprocesses started below.
SRC_DIR = str(pathlib.Path(models.__file__).resolve().parents[2])

MODEL_NAMES = [
    name for name in models.__all__ if hasattr(getattr(models, name), "model_fields")
]


@pytest.mark.parametrize("name", MODEL_NAMES)
def test_model_is_fully_defined(name):
    """Every exported model resolves its annotations at import time."""
    model = getattr(models, name)
    assert model.__pydantic_complete__, (
        f"{name} has unresolved forward references. Add it to the "
        f"model_rebuild() loop at the bottom of aircall/models/__init__.py."
    )


@pytest.mark.parametrize(
    "first_import",
    [
        "aircall.models.user",
        "aircall.models.number",
        "aircall.models.call",
        "aircall.models.message",
        "aircall.models.integration",
        "aircall.resources.user",
        "aircall",
    ],
)
def test_models_resolve_regardless_of_import_order(first_import):
    """Resolution must not depend on which module the caller imports first.

    Runs in a clean interpreter so a previously-populated sys.modules cannot
    mask an ordering problem.
    """
    code = (
        f"import {first_import}\n"
        "from aircall.models import User, Call, Team, Message, Integration\n"
        "for m in (User, Call, Team, Message, Integration):\n"
        "    assert m.__pydantic_complete__, m.__name__\n"
    )
    env = dict(os.environ, PYTHONPATH=SRC_DIR)
    result = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True, text=True, check=False, env=env,
    )
    assert result.returncode == 0, (
        f"importing {first_import} first left models unresolved:\n{result.stderr}"
    )


def test_user_validates_without_number_in_calling_scope():
    """Validation must not rely on the caller happening to have Number in scope.

    Resource modules import only the models they return, so Number is not in
    their namespace. Constructing User from such a scope is the real-world path
    that failed.
    """
    from aircall.models import User  # deliberately without Number
    from tests.payloads import USER_FULL

    assert User(**USER_FULL).id == 456
