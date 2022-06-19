import json
import os

from utils import GoogleMaps, JSONFile

from fuel_lk.base import Git
from fuel_lk.common import DIR_DATA, GIT_REPO_URL, log
from fuel_lk.workflows import common_workflows


def get_base(extended_shed):
    return dict(
        shed_id=extended_shed['shed_id'],
        shed_code=extended_shed['shed_code'],
        shed_name=extended_shed['shed_name'],
        shed_type=extended_shed['shed_type'],
        address=extended_shed['address'],
        lat_lng=extended_shed['lat_lng'],
        gmaps_address=extended_shed['gmaps_address'],
    )


if __name__ == '__main__':
    git = Git(GIT_REPO_URL)
    git.clone(DIR_DATA, force=True)
    git.checkout('data')

    gmaps = GoogleMaps()

    extended_shed_list = common_workflows.get_extended_shed_list()
    extended_shed_list = extended_shed_list
    base_shed_list = []
    n = len(extended_shed_list)
    for i, extended_shed in enumerate(extended_shed_list):
        i1 = i + 1
        log.debug(f'{i1}/{n}) ', extended_shed['shed_name'])
        if 'gmaps_address' not in extended_shed:
            if extended_shed['lat_lng'] == [0, 0]:
                gmaps_address = '[Invalid LatLng]'
            else:
                log.info('gmaps_address not in ' + extended_shed['shed_name'])
                try:
                    gmaps_address = gmaps.get_address(extended_shed['lat_lng'])
                except IndexError:
                    gmaps_address = '[Could not find]'

                if not gmaps_address:
                    log.warning(
                        "No gmaps address for "
                        + extended_shed['shed_name']
                        + json.dumps(extended_shed['lat_lng']))
                    break

            extended_shed['gmaps_address'] = gmaps_address
            log.debug(extended_shed['shed_name'] + '->' + gmaps_address)

        base_shed = get_base(extended_shed)
        base_shed_list.append(base_shed)

    base_shed_list_file = os.path.join(DIR_DATA, 'base_shed_list.json')
    JSONFile(base_shed_list_file).write(base_shed_list)
    n_base_shed_list = len(base_shed_list)
    log.info(f'Wrote {n_base_shed_list} sheds to {base_shed_list_file}')

    git.add_and_commit(f'[{__file__}] Added base_shed_list')
    git.push()

    url = 'https://github.com/nuuuwan/fuel_lk/blob/data/base_shed_list.json'
    os.system(f'open -a safari {url}')
