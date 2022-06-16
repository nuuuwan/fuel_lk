import os

from utils import File, JSONFile, timex

from fuel_lk.common import DIR_DATA, log
from fuel_lk.scraper import shed_scraper, shed_status_scraper

MAX_UPDATE_DELAY_H = 24
DIR_HISTORY = os.path.join(DIR_DATA, 'history')
DIR_LATEST = os.path.join(DIR_DATA, 'latest')


def scrape_sheds():
    shed_list = shed_scraper.scrape_sheds()
    n_shed_list = len(shed_list)
    log.info(f'Scraed {n_shed_list} sheds')
    return shed_list


def filter_by_time(shed):
    time_last_updated_by_shed_ut = shed['time_last_updated_by_shed_ut']
    if not time_last_updated_by_shed_ut:
        return False
    delta_t = timex.get_unixtime() - time_last_updated_by_shed_ut
    return delta_t < MAX_UPDATE_DELAY_H * timex.SECONDS_IN.HOUR


def write_extended_shed(extended_shed):
    shed_code = extended_shed['shed_code']
    json_file = os.path.join(
        DIR_LATEST,
        f'extended_shed.{shed_code}.json',
    )
    JSONFile(json_file).write(extended_shed)
    log.debug(f'Wrote {json_file}')


def scrape_and_write_shed_statuses(shed_list):
    n_shed_list = len(shed_list)
    extended_shed_list = []
    for i, shed in enumerate(shed_list):
        shed_status = shed_status_scraper.scrape_shed_status(
            shed,
            i,
            n_shed_list,
        )
        extended_shed = shed | shed_status
        write_extended_shed(extended_shed)
        extended_shed_list.append(extended_shed)

    return extended_shed_list


def write_LEGACY(shed_status_list):
    n_shed_status_list = len(shed_status_list)
    json_file = os.path.join(DIR_DATA, 'latest/shed_status_list.all.json')
    JSONFile(json_file).write(shed_status_list)
    log.info(f'Saved {n_shed_status_list} sheds to {json_file}')


def copy_latest_to_history():
    time_id = timex.get_time_id()
    dir_history_item = os.path.join(DIR_HISTORY, time_id)
    os.system(f'mkdir {dir_history_item}')
    os.system(f'cp -r {DIR_LATEST}/* {dir_history_item}/')
    log.info(f"Saved {DIR_LATEST} to {dir_history_item}")
    return time_id


def write_readme(shed_list, time_id):
    n_shed_list = len(shed_list)
    lines = [
        '# Fuel.LK',
        f'*Last updated at {time_id}*',
        f'Analyzed {n_shed_list} sheds.',
    ]
    readme_file = os.path.join(DIR_DATA, 'README.md')
    File(readme_file).write('\n\n'.join(lines))
    log.info(f'Wrote {readme_file}')
