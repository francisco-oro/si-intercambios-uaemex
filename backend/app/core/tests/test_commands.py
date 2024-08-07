"""
Test custom python base command
"""
from unittest.mock import patch

from psycopg2 import OperationalError as PostgresOperationalError

from django.core.management import call_command
from django.test import SimpleTestCase
from django.db.utils import OperationalError


@patch('core.management.commands.wait_for_db.Command.check')
class CommandsTests(SimpleTestCase):
    """Test for custom commands."""

    def test_wait_for_db_ready(self, mock_check):
        """Test waiting for db ready."""
        mock_check.return_value = True
        call_command('wait_for_db')
        mock_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, mock_sleep, mock_check):
        """Test waiting for database when getting OperationalError"""
        mock_check.side_effect = [PostgresOperationalError] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')
        self.assertEqual(mock_check.call_count, 6)
