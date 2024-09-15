import pytest
from PyQt6.QtWidgets import QApplication
from ui.components.interval_settings import IntervalSettingsWidget

@pytest.fixture
def app(qapp):
    return qapp

class TestIntervalSettingsWidget:
    def test_initialization(self, app):
        interval_settings = IntervalSettingsWidget()
        assert interval_settings is not None

    def test_initial_values(self, app):
        interval_settings = IntervalSettingsWidget()
        assert interval_settings.get_interval() == 30
        assert interval_settings.interval_slider.value() == 30
        assert interval_settings.interval_input.text() == "30"

    def test_set_interval(self, app):
        interval_settings = IntervalSettingsWidget()
        interval_settings.set_interval(15)
        assert interval_settings.get_interval() == 15
        assert interval_settings.interval_slider.value() == 15
        assert interval_settings.interval_input.text() == "15"

    def test_update_interval_slider(self, app):
        interval_settings = IntervalSettingsWidget()
        interval_settings.interval_input.setText("45")
        assert interval_settings.get_interval() == 45
        assert interval_settings.interval_slider.value() == 45

    def test_update_interval_input(self, app):
        interval_settings = IntervalSettingsWidget()
        interval_settings.interval_slider.setValue(20)
        assert interval_settings.get_interval() == 20
        assert interval_settings.interval_input.text() == "20"

    def test_invalid_interval(self, app):
        interval_settings = IntervalSettingsWidget()
        interval_settings.interval_input.setText("100")
        assert interval_settings.get_interval() == 60  # Max value
        interval_settings.interval_input.setText("0")
        assert interval_settings.get_interval() == 1  # Min value