import logging
import uuid

logger = logging.getLogger("src")

class RequestLogger:
    def __init__(self, request_id: str) -> None:
        self.request_id = request_id

    def _log(self, level, msg, **kwargs):
        kwargs.setdefault("extra", {})['request_id'] = self.request_id
        getattr(logger, level)(msg, **kwargs)

    def info(self, msg, **kwargs):
        self._log("info", msg, **kwargs)

    def warning(self, msg, **kwargs):
        self._log("warning", msg, **kwargs)

    def error(self, msg, **kwargs):
        self._log("error", msg, **kwargs)

    def debug(self, msg, **kwargs):
        self._log("debug", msg, **kwargs)        

