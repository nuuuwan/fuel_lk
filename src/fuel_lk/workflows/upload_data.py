import os

from fuel_lk.common import DIR_DATA
from fuel_lk.scraper import scrape


def before():
    os.system(f'rm -rf {DIR_DATA}')
    os.system(f'mkdir {DIR_DATA}')


def after():
    os.system(f'rm -rf {DIR_DATA}')


def pipeline():
    scrape.scrape_shed_data()


if __name__ == '__main__':
    before()
    pipeline()
    after()
