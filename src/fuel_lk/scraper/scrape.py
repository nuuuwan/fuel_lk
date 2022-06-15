import json
import os

import requests
from utils import TSVFile

from fuel_lk.common import log
from fuel_lk.core import districts

DEFAULT_FUEL_TYPE = 'p92'

URL_API_BASE = 'https://fuel.gov.lk/api/v1/sheddetails'


def scrape_shed_data_for_single_district(
    district_id,
    province_fuel_id,
    district_fuel_id,
):
    url = os.path.join(
        URL_API_BASE, 'search'
    )
    data_json = requests.post(url, json=dict(
        province=province_fuel_id,
        district=district_fuel_id,
        fuelType=DEFAULT_FUEL_TYPE,
    )).text
    shed_data_list = json.loads(data_json)
    n_shed_data_list = len(shed_data_list)

    tsv_file = f'/tmp/fuel_lk.shed_data.{district_id}.tsv'
    TSVFile(tsv_file).write(shed_data_list)

    log.debug(
        f'Saved {n_shed_data_list} sheds for {district_id} to {tsv_file}')


def scrape_shed_data():
    expanded_district_list = districts.get_expanded_district_list()

    for expanded_district in expanded_district_list:
        scrape_shed_data_for_single_district(
            expanded_district['district_id'],
            expanded_district['province_fuel_id'],
            expanded_district['district_fuel_id'],
        )


if __name__ == '__main__':
    scrape_shed_data()
