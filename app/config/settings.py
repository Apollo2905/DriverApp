import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    """Настройки подключения"""
    SCPI_HOST: str = os.getenv("SCPI_HOST", "127.0.0.1")  # IP блока питания
    SCPI_PORT: int = int(os.getenv("SCPI_PORT", 5025))  # порт для SCPI-команд
    API_PORT: int = int(os.getenv("API_PORT", 8000))  # Порт для REST API

    """Характеристики устройства"""
    MAX_CHANNELS: int = 4
    MAX_VOLTAGE: dict = {1: 32.0, 2: 32.0, 3: 5.0, 4: 15.0}
    MAX_CURRENT: dict = {1: 3.0, 2: 3.0, 3: 1.0, 4: 1.0}

    """Настройки логирования"""
    LOG_FILE: str = os.getenv("LOG_FILE", "app/logs/telemetry.log")
    # LOG_FILE_COMMAND: str = os.getenv("LOG_FILE_COMMAND", "app/logs/request_response.log")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    """Интервал опроса телеметрии"""
    TELEMETRY_INTERVAL: float = 15.0

    """Разделитель команд SCPI"""
    SCPI_TERMINATOR: str = "\n"

    """Команды SCPI"""
    COMMAND_SET_VOLTAGE: str = "CH{channel}:VOLTAGE {value}"
    COMMAND_SET_CURRENT: str = "CH{channel}:CURRENT {value}"
    COMMAND_POWER_ON: str = "CH{channel}:STATE ON"
    COMMAND_POWER_OFF: str = "CH{channel}:STATE OFF"
    COMMAND_MEASURE: str = "CH{channel}:MEASURE?"

    def create_log_folder(self):
        # os.makedirs(os.path.dirname(self.LOG_FILE_COMMAND), exist_ok=True)
        os.makedirs(os.path.dirname(self.LOG_FILE), exist_ok=True)


settings = Settings()
settings.create_log_folder()
