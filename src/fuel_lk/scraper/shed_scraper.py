import json
import os

import requests

from fuel_lk.common import DEFAULT_FUEL_TYPE, URL_API_BASE, log
from fuel_lk.core import districts, time_utils


def clean_shed_data(d):
    [
        time_last_updated_by_shed_ut,
        time_last_updated_by_shed,
    ] = time_utils.get_times(d['lastupdatebyshed'])

    eta = eta_ut = eta_amount = None
    if d['eta'] and isinstance(d['eta'], str):
        tokens = d['eta'].split(',')
        if len(tokens) == 2:
            eta_raw, eta_amount = tokens
            [
                eta_ut,
                eta,
            ] = time_utils.get_times(eta_raw)

    return dict(
        shed_id=d['shedId'],
        shed_name=d['shedName'],
        shed_type=d['shedType'],
        time_last_updated_by_shed=time_last_updated_by_shed,
        time_last_updated_by_shed_ut=time_last_updated_by_shed_ut,
        fuel_type=d['fuelType'],
        fuel_capacity=d['fuelCapacity'],
        bowser_distatch=d['bowserDispatch'],
        eta=eta,
        eta_ut=eta_ut,
        eta_amount=eta_amount,
        did_shed_owner_update_today=d['shedownerupdatetoday'],
    )


def scrape_sheds_for_single_district(
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
    shed_list = json.loads(data_json)
    shed_list = list(map(clean_shed_data, shed_list))
    n_shed_list = len(shed_list)
    log.debug(f'Scraped {n_shed_list} sheds for {district_id}')
    return shed_list


def scrape_sheds():
    expanded_district_list = districts.get_expanded_district_list()

    shed_list_all = []
    for expanded_district in expanded_district_list:
        shed_list_all += scrape_sheds_for_single_district(
            expanded_district['district_id'],
            expanded_district['province_fuel_id'],
            expanded_district['district_fuel_id'],
        )
    return shed_list_all


if __name__ == '__main__':
    shed_list = scrape_sheds_for_single_district('LK-11', 1, 1)
    print(shed_list[0])
