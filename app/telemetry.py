import asyncio
import logging
from datetime import datetime
from power_supply_driver import PowerSupplyDriver
from config.settings import settings

logging.basicConfig(
    filename=settings.LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(message)s"
)


class TelemetryLogger:
    def __init__(self, driver: PowerSupplyDriver):
        self.driver = driver

    async def log_telemetry(self):
        while True:
            try:
                telemetry = await self.driver.get_telemetry()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logging.info(f"Телеметрия на {timestamp}: {telemetry}")
            except Exception as e:
                logging.error(f"Ошибка логирования телеметрии: {e}")
            await asyncio.sleep(1)  # Опрос каждую секунду
