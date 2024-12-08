import asyncio
import logging
# from config.settings import settings


class MockDeviceServer:
    def __init__(self, host: str = "127.0.0.1", port: int = 5025):
        self.host = host
        self.port = port
        self.server = None
        self.channels = {
            1: {"voltage": 0.0, "current": 0.0, "state": "OFF"},
            2: {"voltage": 0.0, "current": 0.0, "state": "OFF"},
            3: {"voltage": 0.0, "current": 0.0, "state": "OFF"},
            4: {"voltage": 0.0, "current": 0.0, "state": "OFF"},
        }

    async def handle_client(self, reader, writer):
        while True:
            data = await reader.read(1024)
            if not data:
                break
            command = data.decode().strip()
            response = self.handle_command(command)
            writer.write(response.encode() + b"\n")
            await writer.drain()
        writer.close()

    def handle_command(self, command: str) -> str:
        # Парсим команды SCPI
        if command.startswith("CH"):
            parts = command.split()
            channel = int(command[2])
            if "VOLTAGE" in command:
                value = float(parts[1])
                self.channels[channel]["voltage"] = value
                return f"Напряжение установлено на {value} для канала {channel}"
            elif "CURRENT" in command:
                value = float(parts[1])
                self.channels[channel]["current"] = value
                return f"Ток установлен на {value} для канала {channel}"
            elif "STATE ON" in command:
                self.channels[channel]["state"] = "ON"
                return f"Канал {channel} включен"
            elif "STATE OFF" in command:
                self.channels[channel]["state"] = "OFF"
                return f"Канал {channel} выключен"
            elif "MEASURE?" in command:
                ch_state = self.channels[channel]
                return f"{ch_state['voltage']} В, {ch_state['current']} А, {ch_state['state']}"

    async def start(self):
        self.server = await asyncio.start_server(
            self.handle_client, self.host, self.port
        )
        async with self.server:
            await self.server.serve_forever()


# Запуск мок-устройства
if __name__ == "__main__":
    server = MockDeviceServer()
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        logging.info("Программа завершена пользователем")
