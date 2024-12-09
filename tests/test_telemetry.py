import pytest
from unittest.mock import AsyncMock, MagicMock
from app.telemetry import TelemetryLogger


@pytest.fixture
def mock_driver():
    driver = AsyncMock()
    driver.get_telemetry.return_value = {
        1: {"voltage": 5.0, "current": 1.0, "power": 5.0, "state": "ON"},
        2: {"voltage": 12.0, "current": 2.0, "power": 24.0, "state": "OFF"},
        3: {"voltage": 9.0, "current": 0.5, "power": 4.5, "state": "ON"},
        4: {"voltage": 15.0, "current": 3.0, "power": 45.0, "state": "OFF"},
    }
    return driver


@pytest.mark.asyncio
async def test_log_telemetry(mock_driver):
    # Создаем мок для логгера
    mock_logger = MagicMock()
    telemetry_logger = TelemetryLogger(mock_driver, mock_logger)
    await telemetry_logger.log_telemetry(iterations=5)
    assert mock_driver.get_telemetry.call_count == 5
    # Проверяем, что mock_logger.info вызвался как минимум 5 раз
    assert mock_logger.info.call_count >= 5
