import asyncio
import subprocess


async def start_main():
    """Запуск основного приложения"""
    process = await asyncio.create_subprocess_exec(
        "python", "app/main.py",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    return process


async def start_mock_device():
    """Запускает мок-источник"""
    process = await asyncio.create_subprocess_exec(
        "python", "app/mock_device.py",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    return process


async def main():
    main_app = await start_main()
    mock_device = await start_mock_device()

    try:
        await asyncio.gather(main_app.wait(), mock_device.wait())
    except asyncio.CancelledError:
        main_app.terminate()
        mock_device.terminate()

if __name__ == "__main__":
    asyncio.run(main())
