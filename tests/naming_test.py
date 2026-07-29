import ast
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from pittapi.cal import Event


def test_ordinary_definitions_do_not_start_with_underscore():
    violations = []
    for path in Path("pittapi").glob("*.py"):
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if node.name.startswith("_") and not node.name.startswith("__"):
                    violations.append(f"{path}:{node.lineno} {node.name}")
    assert violations == []


def test_models_are_frozen_and_nested_collections_are_tuples():
    event = Event("2026-01-01", "Title", "Content", ("Academic",))
    with pytest.raises(FrozenInstanceError):
        event.title = "Changed"
    assert isinstance(event.categories, tuple)
