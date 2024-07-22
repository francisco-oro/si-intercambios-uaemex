"""
Django command to wait for database to be available
"""
import time

from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Command to wait for database to be available"""
    def handle(self, *args, **options):
        """Entry point of the command"""
        self.stdout.write('Waiting for database to be available...')
        db_up = False
        while not db_up:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2Error ,OperationalError):
                self.stdout.write('Database not available. Waiting for database to be available...')
                time.sleep(1)
                
            self.stdout.write(self.style.SUCCESS('Database available!'))
            
            
            