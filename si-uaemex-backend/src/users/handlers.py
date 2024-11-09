import logging
from src.common.events import EventHandler
from .services import EmailService

logger = logging.getLogger(__name__)

def handle_user_created(user):
    logger.info(f"Handling user_created event for user: {user.email}")
    try:
        EmailService.send_activation_email(user)
        logger.info(f"Successfully processed user_created event for user: {user.email}")
    except Exception as e:
        logger.error(f"Failed to process user_created event for user {user.email}: {str(e)}")
        raise

# Register the handler when this module is imported
logger.info("Registering user_created event handler")
EventHandler.register('user_created', handle_user_created)
