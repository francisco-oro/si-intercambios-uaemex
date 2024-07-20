"""
Django command to wait for database to be available
"""

from django.core.management import BaseCommand

class WaitForDBCommand(BaseCommand):
    """Command to wait for database to be available"""
    def handle(self, *args, **options)->bool:
        # Argument
        return True
        # return False
