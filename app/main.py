import asyncio
from app.api import app
from app.telemetry import TelemetryLogger
from app.power_supply_driver import PowerSupplyDriver
from app.scpi_client import SCPIClient
from app.config.settings import settings
from dotenv import load_dotenv
import uvicorn
import logging

load_dotenv()

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
        logging.info("Начало логирования телеметрии")
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
