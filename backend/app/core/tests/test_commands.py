"""
Test custom python base command
"""

from unittest.mock import patch

from psycopg2 import OperationalError as PsycopgOperationalError 


from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

@patch('core.management.commands.base.BaseCommand.handle')
class CommandsTests(SimpleTestCase):
    """Test for custom commands."""
    
    def test_wait_for_db_ready(self):
        """Test waiting for db ready."""
        pass