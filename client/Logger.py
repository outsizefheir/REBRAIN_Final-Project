import logging

def logger(log_file='log_file.log'):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s: %(levelname)s - %(message)s',
        encoding='utf-8',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )