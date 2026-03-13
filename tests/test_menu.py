"""
Basic smoke tests for the core menu module.
"""

import unittest
from unittest.mock import patch
from io import StringIO
from core.menu import display_menu


class TestDisplayMenu(unittest.TestCase):
    """Verify the menu renderer outputs expected strings."""

    def test_menu_contains_title(self):
        options = [{"key": "1", "label": "Play"}, {"key": "q", "label": "Quit"}]
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            display_menu("Test Menu", options)
            output = mock_out.getvalue()
        self.assertIn("TEST MENU", output)

    def test_menu_contains_option_labels(self):
        options = [{"key": "1", "label": "First"}, {"key": "2", "label": "Second"}]
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            display_menu("Demo", options)
            output = mock_out.getvalue()
        self.assertIn("First", output)
        self.assertIn("Second", output)


if __name__ == "__main__":
    unittest.main()
