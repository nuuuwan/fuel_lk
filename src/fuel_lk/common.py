import os

from utils import logx

DEFAULT_FUEL_TYPE = 'p92'

DIR_DATA = '/tmp/fuel_lk'
DIR_DATA_HISTORY = os.path.join(DIR_DATA, 'history')
DIR_DATA_LATEST = os.path.join(DIR_DATA, 'latest')

URL_API_BASE = 'https://fuel.gov.lk/api/v1/sheddetails'

log = logx.get_logger('fuel_lk')
