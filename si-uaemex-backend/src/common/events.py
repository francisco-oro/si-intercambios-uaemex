from typing import Callable
from collections import defaultdict

import logging

logger = logging.getLogger(__name__)

class EventHandler:
    _handlers = defaultdict(list)

    @classmethod
    def register(cls, event_name: str, handler: Callable):
        cls._handlers[event_name].append(handler)
        logger.info(f"Registered handler {handler.__name__} for event {event_name}")

    @classmethod
    def dispatch(cls, event_name: str, *args, **kwargs):
        logger.info(f"Dispatching event: {event_name}")
        if event_name in cls._handlers:
            for handler in cls._handlers[event_name]:
                try:
                    logger.debug(f"Executing handler {handler.__name__} for event {event_name}")
                    handler(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Error in handler {handler.__name__} for event {event_name}: {str(e)}")
                    raise
        else:
            logger.warning(f"No handlers registered for event: {event_name}")