import json
import os

import requests

from fuel_lk.common import DEFAULT_FUEL_TYPE, URL_API_BASE, log
from fuel_lk.core import time_utils


def clean_dispatch_schedule(d):
    time_dispatch_ut, time_dispatch = time_utils.get_times(d['dispatchTime'])
    time_last_updated_ut, time_last_updated = time_utils.get_times(
        d['lastupdateTime'])
    time_eta_ut, time_eta = time_utils.get_times(d['eta'])

    return dict(
        time_dispatch_ut=time_dispatch_ut,
        time_dispatch=time_dispatch,
        fuel_type=d['fuelType'],
        plant_name=d['plantName'],
        amount=d['amountDispatch'],
        time_last_updated_ut=time_last_updated_ut,
        time_last_updated=time_last_updated,
        time_eta_ut=time_eta_ut,
        time_eta=time_eta,
    )


def clean_shed_status(d):
    time_last_updated_ut, time_last_updated = time_utils.get_times(
        d['lastupdateddate'])

    return dict(
        shed_name=d['shedName'],
        shed_code=d['shedCode'],
        address=d['address'],
        lat_lng=list(map(
            lambda x: (float)(x),
            [d['longitude'], d['latitude']],
        )),
        time_last_updated_ut=time_last_updated_ut,
        time_last_updated=time_last_updated,
        browser_dispatch=d['bowserDispatch'],
        did_shed_owner_update_today=d['shedownerupdatetoday'],
        dispatch_schedule_list=list(map(
            clean_dispatch_schedule,
            d['dispatchSheduleList'] if d['dispatchSheduleList'] else [],
        )),
        fuel_status_idx=dict(
            p92=dict(
                is_available=d['p92Availablity'],
                capacity=d['p92Capacity'],
            ),
            p95=dict(
                is_available=d['p95Availablity'],
                capacity=d['p95Capacity'],
            ),
            d=dict(
                is_available=d['davailablity'],
                capacity=d['dcapacity'],
            ),
            sd=dict(
                is_available=d['sdavailablity'],
                capacity=d['sdcapacity'],
            ),
            k=dict(
                is_available=d['kavailablity'],
                capacity=d['kcapacity'],
            ),
            ik=dict(
                is_available=d['ikavailablity'],
                capacity=d['ikcapacity'],
            )
        )
    )


def scrape_shed_status(shed_data, i, n):
    shed_id = shed_data['shed_id']
    url = os.path.join(
        URL_API_BASE, f'{shed_id}/{DEFAULT_FUEL_TYPE}'
    )
    try:
        data_json = requests.get(url).text
        data = json.loads(data_json)
    except Exception as e:
        log.error(f'Fetch from {url} failed')
        log.error(str(e))
        return None

    data = shed_data | clean_shed_status(data)
    i1 = i + 1
    log.debug(f'{i1}/{n}) Scraped shed status for {shed_id=}')
    return data


if __name__ == '__main__':
    print(json.dumps(
        scrape_shed_status(
            {
                "shed_id": 29,
                "shed_name": "NAFT, MATTAMAGODA-KOTIYAKUMBURA",
                "time_last_updated_by_shed": "2022-06-15 07:44:00",
                "time_last_updated_by_shed_ut": 1655259240,
                "fuel_type": "p92",
                "fuel_capacity": 900.0,
                "bowser_distatch": True,
                "eta": None,
                "did_shed_owner_update_today": True,
            },
            0,
            1,
        ),
        indent=2))
