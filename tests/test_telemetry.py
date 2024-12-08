import pytest
from unittest.mock import AsyncMock
from app.telemetry import TelemetryLogger


@pytest.fixture
def mock_driver():
    driver = AsyncMock()
    driver.get_telemetry.return_value = {"voltage": 5.0, "current": 1.0, "state": "ON"}
    return driver


@pytest.mark.asyncio
async def test_log_telemetry(mock_driver):
    telemetry_logger = TelemetryLogger(mock_driver)
    await telemetry_logger.log_telemetry(iterations=5)
    assert mock_driver.get_telemetry.call_count == 5
