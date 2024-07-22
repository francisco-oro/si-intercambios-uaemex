"""
Test custom python base command
"""
from django.test import SimpleTestCase

class CommandsTests(SimpleTestCase):
    """Test for custom commands."""
    
    def test_wait_for_db_ready(self):
        """Test waiting for db ready."""
