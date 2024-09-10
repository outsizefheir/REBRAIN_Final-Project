import requests
import platform
import os 
import json
import asyncio
from aiohttp import ClientSession
from Logger import logger
import logging

logger()

class Connect:
    def __init__(self, url_serv):
        self.url = url_serv
        self.external_ip = self.external_ip()
        self.hostname = self.hostname()
        self.description = self.description()
    logging.info('Собранны данные о сервере')
    
    def external_ip(self):
        return requests.get('https://ifconfig.me/ip').text
    
    def hostname(self):
        return platform.node()
        
    def description(self):
        return os.getenv('USERNAME')
    
    async def registered(self):
        data = {
            'name': self.hostname,
            'description': self.description,
            'ip_address': self.external_ip,
        }
        logging.info("Регистрация сервера: %s", data)

        async with ClientSession() as session:
            while True:
                try:
                    async with session.post(f'{self.url}/api/servers/add', json=data) as response:
                        response_text = await response.text()
                        if response.status >= 200 | response.status <= 300:
                            logging.info(f'Сервер успешно зарегистрирован: статус={response.status}, ответ={response_text}')
                        else:
                            logging.error(f'Ошибка при регистрации сервера: статус={response.status}, ответ={response_text}')
                except Exception as e:
                    logging.error(f'Ошибка при отправке запроса регистрации: {e}')

                await asyncio.sleep(60)
            