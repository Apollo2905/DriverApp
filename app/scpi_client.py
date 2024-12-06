import asyncio
import logging


class SCPIClient:
    def __init__(self, host: str, port: int, buffer_size: int = 4096):
        self.port = port
        self.host = host
        self.buffer_size = buffer_size

    async def send_command(self, command: str) -> str:
        try:
            logging.info(f"Отправка команды: {command}")
            reader, writer = await asyncio.open_connection(self.host, self.port)
            writer.write(f"{command}\n".encode())
            await writer.drain()
            response = await reader.read(self.buffer_size)
            writer.close()
            await writer.wait_closed()
            logging.info(f"Получен ответ: {response.decode().strip()}")
            return response.decode().strip()
        except (asyncio.TimeoutError, ConnectionError) as e:
            logging.error(f"Ошибка отправки команды '{command}': {e}")
            raise
