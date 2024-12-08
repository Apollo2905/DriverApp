import asyncio
import logging
from datetime import datetime
from app.power_supply_driver import PowerSupplyDriver
from app.config.settings import settings

logging.basicConfig(
    filename=settings.LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(message)s"
)


class TelemetryLogger:
    def __init__(self, driver: PowerSupplyDriver):
        self.driver = driver
        self._running = False  # Флаг для управления циклом

    async def log_telemetry(self, iterations: int = None):
        """
        Логирует телеметрию. Если передан `iterations`, выполняет указанное количество итераций.
        В противном случае работает в бесконечном цикле.
        """
        self._running = True
        count = 0
        while self._running:
            try:
                telemetry = await self.driver.get_telemetry()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logging.info(f"Телеметрия на {timestamp}: {telemetry}")
            except Exception as e:
                logging.error(f"Ошибка логирования телеметрии: {e}")
            await asyncio.sleep(settings.TELEMETRY_INTERVAL)

            if iterations is not None:
                count += 1
                if count >= iterations:
                    break

    def stop(self):
        """Останавливает бесконечный цикл."""
        self._running = False
