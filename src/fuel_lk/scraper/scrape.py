import json
import os

import requests
from utils import JSONFile, timex

from fuel_lk.common import DIR_DATA, log
from fuel_lk.core import districts

DEFAULT_FUEL_TYPE = 'p92'

URL_API_BASE = 'https://fuel.gov.lk/api/v1/sheddetails'


def clean_shed_data(d):
    try:
        time_last_updated_by_shed_ut = timex.parse_time(
            d['lastupdatebyshed'],
            '%Y-%m-%d %H:%M',
        )
        time_last_updated_by_shed = timex.format_time(
            time_last_updated_by_shed_ut)
    except ValueError:
        time_last_updated_by_shed_ut = None
        time_last_updated_by_shed = None

    return dict(
        shed_id=d['shedId'],
        shed_name=d['shedName'],
        time_last_updated_by_shed=time_last_updated_by_shed,
        time_last_updated_by_shed_ut=time_last_updated_by_shed_ut,
        fuel_type=d['fuelType'],
        fuel_capacity=d['fuelCapacity'],
        bowser_distatch=d['bowserDispatch'],
        eta=d['eta'],
        did_shed_owner_update_today=d['shedownerupdatetoday'],
    )


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
    shed_data_list = list(map(clean_shed_data, shed_data_list))
    n_shed_data_list = len(shed_data_list)

    json_file = os.path.join(DIR_DATA, f'latest/shed_data.{district_id}.json')
    JSONFile(json_file).write(shed_data_list)
    log.debug(
        f'Saved {n_shed_data_list} sheds for {district_id} to {json_file}')

    return shed_data_list


def scrape_shed_data():
    expanded_district_list = districts.get_expanded_district_list()

    shed_data_list_all = []
    for expanded_district in expanded_district_list[-1:]:
        shed_data_list_all += scrape_shed_data_for_single_district(
            expanded_district['district_id'],
            expanded_district['province_fuel_id'],
            expanded_district['district_fuel_id'],
        )

    n_shed_data_list_all = len(shed_data_list_all)
    json_file = os.path.join(DIR_DATA, 'latest/shed_data.all.json')
    JSONFile(json_file).write(shed_data_list_all)
    log.info(
        f'Saved {n_shed_data_list_all} sheds to {json_file}')

    return shed_data_list_all