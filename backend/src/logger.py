import logging

logger = (
   logging.getLogger("uvicorn.error")
)


def log_info_flush(msg, *args, **kwargs):
    """
    Log an info message and flush the logger.
    This is useful for ensuring that log messages are immediately written out,
    especially in environments where logs are monitored in real-time.
    """
    logger.info(msg, *args, **kwargs)
    for handler in logger.handlers:
        handler.flush()
