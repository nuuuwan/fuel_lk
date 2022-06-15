import os

from utils import logx

DIR_DATA = '/tmp/fuel_lk'
DIR_DATA_HISTORY = os.path.join(DIR_DATA, 'history')
DIR_DATA_LATEST = os.path.join(DIR_DATA, 'latest')

log = logx.get_logger('fuel_lk')
