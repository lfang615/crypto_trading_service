import pytest
from app.core.logging import AsyncLogger

def test_singleton_logger():
    # Test that the logger is a singleton
    logger1 = AsyncLogger().get_logger()
    logger2 = AsyncLogger().get_logger()
    assert logger1 == logger2