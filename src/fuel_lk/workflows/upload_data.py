import os

from utils import File, timex

from fuel_lk.common import DIR_DATA, DIR_DATA_HISTORY, DIR_DATA_LATEST, log
from fuel_lk.scraper import shed_scraper, shed_status_scraper

MAX_UPDATE_DELAY_H = 3


def before():
    os.system(f'rm -rf {DIR_DATA}')
    os.system(f'mkdir {DIR_DATA}')
    os.system(f'mkdir {DIR_DATA_LATEST}')
    os.system(f'mkdir {DIR_DATA_HISTORY}')


def after(shed_list_all, shed_status_list):
    time_id = timex.get_time_id()
    dir_history_item = os.path.join(DIR_DATA_HISTORY, time_id)
    os.system(f'cp -r {DIR_DATA}/latest {dir_history_item}')
    log.info(f"Saved latest to {dir_history_item}")

    n_shed_list_all = len(shed_list_all)

    lines = [
        '# Fuel.LK',
        f'*Last updated at {time_id}*',
        f'Analyzed {n_shed_list_all} sheds.',
        '## Latest Shed Updates ',
        f'(*Sheds that updated data in the last {MAX_UPDATE_DELAY_H} hours*)',
    ] + list(map(lambda shed: '* [%s] %s (%s)' % (
        shed['shed_code'],
        shed['shed_name'],
        shed['address'],
    ),
        shed_status_list,
    ))
    readme_file = os.path.join(DIR_DATA, 'README.md')
    File(readme_file).write('\n\n'.join(lines))
    log.info(f'Saved {readme_file}')


def filter_by_time(shed):
    time_last_updated_by_shed_ut = shed['time_last_updated_by_shed_ut']
    if not time_last_updated_by_shed_ut:
        return False
    delta_t = timex.get_unixtime() - time_last_updated_by_shed_ut
    return delta_t < MAX_UPDATE_DELAY_H * timex.SECONDS_IN.HOUR


def pipeline():
    shed_list_all = shed_scraper.scrape_sheds()
    filtered_shed_data_list_all = list(filter(
        filter_by_time,
        shed_list_all,
    ))
    n_filtered_shed_data_list_all = len(filtered_shed_data_list_all)
    log.info(
        f'Found {n_filtered_shed_data_list_all} updated ' +
        f'in the last {MAX_UPDATE_DELAY_H} hours')
    shed_status_list = shed_status_scraper.scrape_shed_statuses(
        filtered_shed_data_list_all)
    return [shed_list_all, shed_status_list]


if __name__ == '__main__':
    before()
    [shed_list_all, shed_status_list] = pipeline()
    after(shed_list_all, shed_status_list)
