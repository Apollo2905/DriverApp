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

# Логгер для телеметрии
telemetry_logging = logging.getLogger("telemetry")
telemetry_logging.setLevel(logging.INFO)
telemetry_handler = logging.FileHandler(settings.LOG_FILE_TELEMETRY)
telemetry_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
telemetry_logging.addHandler(telemetry_handler)

telemetry_logging.propagate = False

# Основной логгер для общего логирования
logging.basicConfig(
    filename=settings.LOG_FILE_COMMAND,
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s - %(levelname)s - %(message)s"
)

client = SCPIClient(settings.SCPI_HOST, settings.SCPI_PORT)
driver = PowerSupplyDriver(client)
telemetry_logger = TelemetryLogger(driver, telemetry_logging)


async def start_telemetry():
    try:
        telemetry_logging.info("Начало логирования телеметрии")
        print("Начало логирования телеметрии...")
        await telemetry_logger.log_telemetry()
    except Exception as e:
        telemetry_logging.error(f"Логирование телеметрии завершилось с ошибкой: {e}")


async def main():
    """
    Основная точка запуска приложения. Одновременно запускает сервер и задачу телеметрии.
    """
    # Создаем задачу для телеметрии
    asyncio.create_task(start_telemetry())

    # Запускаем сервер Uvicorn
    config = uvicorn.Config(app, host="0.0.0.0", port=settings.API_PORT, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
