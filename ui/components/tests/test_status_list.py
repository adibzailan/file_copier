import pytest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QColor
from ui.components.status_list import StatusListWidget

@pytest.fixture
def app(qapp):
    return qapp

class TestStatusListWidget:
    def test_initialization(self, app):
        status_list = StatusListWidget()
        assert status_list is not None
        assert status_list.status_list.count() == 0

    def test_add_status(self, app):
        status_list = StatusListWidget()
        status_list.add_status("Test status")
        assert status_list.status_list.count() == 1
        assert status_list.status_list.item(0).text() == "Test status"
        assert status_list.status_list.item(0).foreground().color() == QColor("#333333")

    def test_add_important_status(self, app):
        status_list = StatusListWidget()
        status_list.add_status("Important status", is_important=True)
        assert status_list.status_list.count() == 1
        assert status_list.status_list.item(0).text() == "Important status"
        assert status_list.status_list.item(0).foreground().color() == QColor("#FF6F61")

    def test_multiple_statuses(self, app):
        status_list = StatusListWidget()
        status_list.add_status("Status 1")
        status_list.add_status("Status 2")
        status_list.add_status("Status 3", is_important=True)
        assert status_list.status_list.count() == 3
        assert status_list.status_list.item(0).text() == "Status 1"
        assert status_list.status_list.item(1).text() == "Status 2"
        assert status_list.status_list.item(2).text() == "Status 3"
        assert status_list.status_list.item(2).foreground().color() == QColor("#FF6F61")

    def test_clear_status(self, app):
        status_list = StatusListWidget()
        status_list.add_status("Status 1")
        status_list.add_status("Status 2")
        assert status_list.status_list.count() == 2
        status_list.clear_status()
        assert status_list.status_list.count() == 0

    def test_scrolling(self, app):
        status_list = StatusListWidget()
        for i in range(100):
            status_list.add_status(f"Status {i}")
        assert status_list.status_list.count() == 100
        assert status_list.status_list.verticalScrollBar().value() == status_list.status_list.verticalScrollBar().maximum()