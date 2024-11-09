from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.users'

    def ready(self):
        try:
            logger.info("Registering user event handlers...")
            # Import the handlers module to register the handlers
            from src.users import handlers  # This will execute the registration code
            logger.info("User event handlers registered successfully")
        except Exception as e:
            logger.error(f"Failed to register user event handlers: {str(e)}")
