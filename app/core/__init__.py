from .config import Settings
from .logging_config import AsyncLogger

settings = Settings()
logger = AsyncLogger()

__all__ = ['settings', 'logger']
