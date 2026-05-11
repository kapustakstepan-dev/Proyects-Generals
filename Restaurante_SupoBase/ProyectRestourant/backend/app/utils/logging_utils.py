import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
        }
        if hasattr(record, "event"):
            log_record["event"] = record.event
        if hasattr(record, "user_id"):
            log_record["user_id"] = record.user_id
        return json.dumps(log_record)

def setup_logger():
    logger = logging.getLogger("RestauranteSupoBase")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)
    return logger

logger = setup_logger()

def log_event(event_name, message, user_id=None):
    extra = {"event": event_name}
    if user_id:
        extra["user_id"] = user_id
    logger.info(message, extra=extra)
