import psutil as ps
import platform
import json
from aiohttp import ClientSession
from Logger import logger
import logging
import asyncio

logger()


class SystemInformation:
    def __init__(self, url_serv):
        self.url = url_serv
        self.sys_info = {
            'host_information': self.host_information(),
            'network': self.network_info(),
            'disk': self.disk_info(),
            'memory': self.memory_info(),
            'cpu': self.cpu_info(),
            'load_average': self.load_average()
        }
        logging.info('Собранны данные о системе')

    def host_information(self):
        uname_res = platform.uname()._asdict()
        del uname_res['release']
        del uname_res['version']
        del uname_res['processor']
        return uname_res

    def network_info(self):
        counters = ps.net_io_counters(pernic=True)
        addrs = ps.net_if_addrs()
        stats = ps.net_if_stats()

        network = {}
        for interface in set(counters.keys()).union(addrs.keys()).union(stats.keys()):
            network[interface] = {}
            
            if interface in counters:
                network[interface].update(counters[interface]._asdict())

            if interface in addrs:
                network[interface]['addresses'] = [addr._asdict() for addr in addrs[interface]]
            
            if interface in stats:
                network[interface].update(stats[interface]._asdict())
        return network
    
    def disk_info(self):
        disk = {}
        partitions = ps.disk_partitions()

        for partition in partitions:
            mountpoint = partition.mountpoint 
            usage = ps.disk_usage(mountpoint)
            
            disk[mountpoint] = {
                'device': partition.device,
                'file_system_type': partition.fstype,
                'total': usage.total,
                'used': usage.used,
                'free': usage.free,
                'percent': usage.percent,
                'opts': partition.opts
            }
        return disk
    
    def memory_info(self):
        return ps.virtual_memory()._asdict()

    def cpu_info(self):
        return {
            'cpu_cores': ps.cpu_count(logical=True),
            'cpu_physical_cores': ps.cpu_count(logical=False),
            'cpu_frequency': ps.cpu_freq(percpu=True)
        }

    def load_average(self):
        return {
            '1 min': ps.getloadavg()[0],
            '5 min': ps.getloadavg()[1],
            '15 min': ps.getloadavg()[2]
        }
        
    def save_to_file(self, filepath='system_info.json'):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.sys_info, f, ensure_ascii=False, indent=4)
            
    async def give_system_info(self):
        data = self.sys_info
        data['server'] = platform.node()

        async with ClientSession() as session:
            while True:
                try:
                    async with session.post(f'{self.url}/api/servers/add_data', json=data) as response:
                        response_text = await response.text()
                        if response.status >= 200 | response.status <= 300:
                            logging.info(f"Сервер успешно отправил данные о системе: статус={response.status}, ответ={response_text}")
                        else:
                            logging.error(f"Ошибка при отправке данных о системе: статус={response.status}, ответ={response_text}")
                except Exception as e:
                    logging.error(f"Ошибка при отправке запроса об отправке данных о системе: {e}")

                await asyncio.sleep(60)