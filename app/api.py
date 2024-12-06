from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from scpi_client import SCPIClient
from power_supply_driver import PowerSupplyDriver
from config.settings import settings
import logging

app = FastAPI()

client = SCPIClient(settings.SCPI_HOST, settings.SCPI_PORT)
driver = PowerSupplyDriver(client)


# Класс для валидации входных данных
class ChannelSettings(BaseModel):
    voltage: float
    current: float

    # Валидатор для напряжения
    @field_validator('voltage')
    def validate_voltage(cls, value, channel: int):
        max_voltage = settings.MAX_VOLTAGE.get(channel, 32.0)  # максимальное напряжение для канала
        if value > max_voltage:
            raise ValueError(f"Для канала {channel} максимальное напряжение {max_voltage} В")
        return value

    # Валидатор для тока
    @field_validator('current')
    def validate_current(cls, value, channel: int):
        max_current = settings.MAX_CURRENT.get(channel, 3.0)  # максимальный ток для канала
        if value > max_current:
            raise ValueError(f"Для канала {channel} максимальный ток {max_current} А")
        return value


@app.post("/channel/{channel}/on")
async def power_on(channel: int, settings: ChannelSettings):
    try:
        await driver.set_current(channel, settings.current)
        await driver.set_voltage(channel, settings.voltage)
        result = await driver.power_on(channel)
        return {"message": "Канал включен", "Результат": result}
    except ValueError as e:
        logging.error(f"Ошибка включения канала {channel}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/channel/{channel}/off")
async def power_off(channel: int):
    try:
        result = await driver.power_off(channel)
        return {"message": "Канал выключен", "Результат": result}
    except ValueError as e:
        logging.error(f"Ошибка выключения канала {channel}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/channel/{channel}/state")
async def get_channel_states(channel: int):
    try:
        state = await driver.measure_state(channel)
        # Парсинг ответа для удобства
        parsed_state = {"raw": state}
        return {"Канал": channel, "Состояние": parsed_state}
    except ValueError as e:
        logging.error(f"Ошибка при получении состояния для канала {channel}: {e}")
        raise HTTPException(status_code=400, detail=str(e))
