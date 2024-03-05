import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(funcName)s:%(message)s')

file_handler1 = logging.FileHandler('activity.log')
file_handler1.setFormatter(formatter)

file_handler2 = logging.FileHandler('errors.log')
file_handler2.setFormatter(formatter)
file_handler2.setLevel(logging.ERROR)

stream_handler = logging.StreamHandler()

logger.addHandler(file_handler1)
logger.addHandler(file_handler2)
logger.addHandler(stream_handler)
