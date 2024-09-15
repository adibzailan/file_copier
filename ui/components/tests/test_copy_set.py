import pytest
from PyQt6.QtWidgets import QApplication
from ui.components.copy_set import CopySetWidget, CopySetManager

@pytest.fixture
def app(qapp):
    return qapp

class TestCopySetWidget:
    def test_initialization(self, app):
        copy_set = CopySetWidget(1)
        assert copy_set is not None
        assert copy_set.set_id == 1

    def test_remove_set(self, app):
        copy_set = CopySetWidget(1)
        removed = False
        def on_removed(widget):
            nonlocal removed
            removed = True
        copy_set.removed.connect(on_removed)
        copy_set.remove_set()
        assert removed

class TestCopySetManager:
    def test_initialization(self, app):
        manager = CopySetManager()
        assert manager is not None
        assert len(manager.copy_sets) == 0

    def test_add_copy_set(self, app):
        manager = CopySetManager()
        manager.add_copy_set()
        assert len(manager.copy_sets) == 1
        assert isinstance(manager.copy_sets[0], CopySetWidget)

    def test_remove_copy_set(self, app):
        manager = CopySetManager()
        manager.add_copy_set()
        assert len(manager.copy_sets) == 1
        manager.remove_copy_set(manager.copy_sets[0])
        assert len(manager.copy_sets) == 0