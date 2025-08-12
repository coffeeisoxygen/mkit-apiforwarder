"""test print settings to terminal and log."""

import logging

from loguru import logger
from pytest import LogCaptureFixture
from src.config import PATHTOENVS


def test_logging_settings(caplog: LogCaptureFixture):
    """Test logging settings."""
    with caplog.at_level(logging.INFO):
        logger.info("Test log message")
        print(f"Using settings from: {PATHTOENVS}")
    assert "Test log message" in caplog.text
