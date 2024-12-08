import pytest
from app.config.settings import settings


@pytest.fixture(autouse=True)
def override_settings():
    settings.SCPI_HOST = "127.0.0.1"
    settings.SCPI_PORT = 5025
    settings.MAX_VOLTAGE = {1: 32.0, 2: 32.0, 3: 5.0, 4: 15.0}
    settings.MAX_CURRENT = {1: 3.0, 2: 3.0, 3: 1.0, 4: 1.0}
