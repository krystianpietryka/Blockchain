import logging
import os
from datetime import datetime
import sys

now_datetime = datetime.now()
now = now_datetime.strftime("%d/%m/%Y %H:%M").replace(' ', '_').replace('/', '_').replace(':', '')
script_dir = str(os.path.dirname(os.path.abspath(__file__)))

log_directory = script_dir + '/Logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

if not os.access(log_directory, os.W_OK):
    raise Exception(f"Permission denied to write to log directory {log_directory}")

error_log_filename = log_directory + f'/error_log_{now}.txt'
execution_log_filename = log_directory + f'/execution_log_{now}.txt'

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger_error = logging.getLogger('logger_error')
logger_error.setLevel(logging.INFO)
error_stream_handler = logging.StreamHandler(sys.stdout)
error_stream_handler.setLevel(logging.INFO)
error_stream_handler.setFormatter(formatter)
logger_error.addHandler(error_stream_handler)
error_file_handler = logging.FileHandler(filename=error_log_filename)
error_file_handler.setLevel(logging.INFO)
error_file_handler.setFormatter(formatter)
logger_error.addHandler(error_file_handler)

logger_info = logging.getLogger('info_logger')
logger_info.setLevel(logging.INFO)
info_stream_handler = logging.StreamHandler(sys.stdout)
info_stream_handler.setLevel(logging.INFO)
info_stream_handler.setFormatter(formatter)
logger_info.addHandler(info_stream_handler)
info_file_handler = logging.FileHandler(filename=execution_log_filename)
info_file_handler.setLevel(logging.INFO)
info_file_handler.setFormatter(formatter)
logger_info.addHandler(info_file_handler)