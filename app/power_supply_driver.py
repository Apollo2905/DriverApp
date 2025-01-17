from app.scpi_client import SCPIClient
import logging
from app.config.settings import settings


class PowerSupplyDriver:
    def __init__(self, client: SCPIClient):
        self.client = client

    async def set_current(self, channel: int, current: float):
        max_current = settings.MAX_CURRENT.get(channel, 3.0)  # Получаем максимальный ток для канала
        if not (0 <= current <= max_current):
            error_message = f"Ток {current} А выходит за пределы (0-{max_current} А) для канала {channel}"
            logging.error(error_message)
            raise ValueError(error_message)
        command = settings.COMMAND_SET_CURRENT.format(channel=channel, value=current)
        logging.info(f"Настройка тока: {command}")
        return await self.client.send_command(command)

    async def set_voltage(self, channel: int, voltage: float):
        max_voltage = settings.MAX_VOLTAGE.get(channel, 32.0)  # Получаем максимальное напряжение для канала
        if not (0 <= voltage <= max_voltage):
            raise ValueError(f"Напряжение {voltage} В выходит за пределы (0-{max_voltage} В) для канала {channel}")
        command = settings.COMMAND_SET_VOLTAGE.format(channel=channel, value=voltage)
        logging.info(f"Настройка напряжения: {command}")
        return await self.client.send_command(command)

    async def power_on(self, channel: int):
        if not (1 <= channel <= settings.MAX_CHANNELS):
            raise ValueError(f"Канал {channel} вне допустимого диапазона (1-{settings.MAX_CHANNELS})")
        command = settings.COMMAND_POWER_ON.format(channel=channel)
        logging.info(f"Включение канала: {channel}")
        return await self.client.send_command(command)

    async def power_off(self, channel: int):
        if not (1 <= channel <= settings.MAX_CHANNELS):
            raise ValueError(f"Канал {channel} вне допустимого диапазона (1-{settings.MAX_CHANNELS})")
        command = settings.COMMAND_POWER_OFF.format(channel=channel)
        logging.info(f"Выключение канала: {channel}")
        return await self.client.send_command(command)

    async def measure_state(self, channel: int):
        if not (1 <= channel <= settings.MAX_CHANNELS):
            raise ValueError(f"Канал {channel} вне допустимого диапазона (1-{settings.MAX_CHANNELS})")
        command = settings.COMMAND_MEASURE.format(channel=channel)
        response = await self.client.send_command(command)
        logging.info(f"Измерение состояния канала {channel}: {response}")
        return response

    async def get_telemetry(self):
        """
        Получает телеметрию по всем каналам.
        Возвращает словарь с данными.
        """
        telemetry_data = {}
        for channel in range(1, settings.MAX_CHANNELS + 1):
            try:
                command = settings.COMMAND_MEASURE.format(channel=channel)
                response = await self.client.send_command(command)

                parts = response.split(",")
                if len(parts) != 3:
                    raise ValueError(f"Некорректный формат ответа: {response}")

                telemetry_data[channel] = {
                    "Напряжение": float(parts[0].strip().split()[0]),
                    "Ток": float(parts[1].strip().split()[0]),
                    "Мощность": float(parts[0].strip().split()[0]) * float(parts[1].strip().split()[0]),
                    "Состояние": parts[2].strip(),
                }
            except Exception as e:
                raise ValueError(f"Ошибка получения данных для канала {channel}: {e}")
        return telemetry_data
