import asyncio
from Connect import Connect
from SystemInformation import SystemInformation
from Logger import logger
import logging

logger()
logging.info("Запуск программы")

async def main():
    connect = Connect('http://127.0.0.1:8000')
    system_info = SystemInformation('http://127.0.0.1:8000')
    
    await asyncio.gather(
        connect.registered(),
        system_info.give_system_info()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error('Критическая ошибка при выполнении программы: {e}')




