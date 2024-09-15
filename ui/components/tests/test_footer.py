import pytest
from ui.components.footer import FooterWidget

class TestFooter:
    def test_initialization(self):
        footer = FooterWidget()
        assert footer is not None

    def test_display_text(self):
        footer = FooterWidget(version="1.2.5")
        assert footer.version == "1.2.5"
        assert "Alpha 1.2.5" in footer.footer_label.text()

    def test_interactive_elements(self):
        footer = FooterWidget()
        assert footer.footer_label.openExternalLinks()
        assert "href" in footer.footer_label.text()