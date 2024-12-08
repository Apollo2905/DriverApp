import pytest
from unittest.mock import AsyncMock
from app.power_supply_driver import PowerSupplyDriver
# from app.config.settings import settings


@pytest.fixture
def mock_client():
    client = AsyncMock()
    return client


@pytest.fixture
def driver(mock_client):
    return PowerSupplyDriver(mock_client)


@pytest.mark.asyncio
async def test_set_voltage(driver, mock_client):
    await driver.set_voltage(1, 5.0)
    mock_client.send_command.assert_called_with("CH1:VOLTAGE 5.0")


@pytest.mark.asyncio
async def test_set_current(driver, mock_client):
    await driver.set_current(1, 1.0)
    mock_client.send_command.assert_called_with("CH1:CURRENT 1.0")


@pytest.mark.asyncio
async def test_power_on(driver, mock_client):
    await driver.power_on(1)
    mock_client.send_command.assert_called_with("CH1:STATE ON")


@pytest.mark.asyncio
async def test_power_off(driver, mock_client):
    await driver.power_off(1)
    mock_client.send_command.assert_called_with("CH1:STATE OFF")
