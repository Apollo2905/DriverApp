import asyncio
from api import app
from telemetry import TelemetryLogger
from power_supply_driver import PowerSupplyDriver
from scpi_client import SCPIClient
from config.settings import settings
import uvicorn
import logging

logging.basicConfig(
    filename=settings.LOG_FILE,
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s - %(levelname)s - %(message)s"
)

client = SCPIClient(settings.SCPI_HOST, settings.SCPI_PORT)
driver = PowerSupplyDriver(client)
telemetry_logger = TelemetryLogger(driver)


async def start_telemetry():
    try:
        print("Начало логирования телеметрии...")
        await telemetry_logger.log_telemetry()
    except Exception as e:
        logging.error(f"Логирование телеметрии завершилось с ошибкой: {e}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    telemetry_task = loop.create_task(start_telemetry())
    telemetry_task.add_done_callback(
        lambda task: logging.error(f"Задача телеметрии завершилась с ошибкой: {task.exception()}")
        if task.exception() else logging.info("Задача телеметрии успешно выполнена")
    )
    uvicorn.run(app, host="0.0.0.0", port=settings.API_PORT)
