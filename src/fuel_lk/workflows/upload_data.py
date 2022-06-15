import os

from utils import timex

from fuel_lk.common import DIR_DATA, DIR_DATA_HISTORY, DIR_DATA_LATEST, log
from fuel_lk.scraper import scrape


def before():
    os.system(f'rm -rf {DIR_DATA}')
    os.system(f'mkdir {DIR_DATA}')
    os.system(f'mkdir {DIR_DATA_LATEST}')
    os.system(f'mkdir {DIR_DATA_HISTORY}')


def after():
    time_id = timex.get_time_id()
    dir_history_item = os.path.join(DIR_DATA_HISTORY, time_id)
    os.system(f'cp -r {DIR_DATA}/latest {dir_history_item}')
    log.info(f"Saved latest to {dir_history_item}")


def pipeline():
    scrape.scrape_shed_data()


if __name__ == '__main__':
    before()
    pipeline()
    after()
