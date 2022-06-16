import os

from utils import File, GoogleMaps, JSONFile, timex

from fuel_lk.base import Git
from fuel_lk.common import DIR_DATA, GIT_REPO_URL, log
from fuel_lk.scraper import shed_scraper, shed_status_scraper

MAX_UPDATE_DELAY_H = 1
DIR_HISTORY = os.path.join(DIR_DATA, 'history')
DIR_LATEST = os.path.join(DIR_DATA, 'latest')


def scrape_sheds():
    shed_list = shed_scraper.scrape_sheds()
    n_shed_list = len(shed_list)
    log.info(f'Scraed {n_shed_list} sheds')
    return shed_list


def write_extended_shed(extended_shed):
    shed_code = extended_shed['shed_code']
    json_file = os.path.join(
        DIR_LATEST,
        f'extended_shed.{shed_code}.json',
    )
    JSONFile(json_file).write(extended_shed)
    log.debug(f'Wrote {json_file}')


def get_shed_data_3p(extended_shed, gmaps):
    gmaps_address = gmaps.get_address(extended_shed['lat_lng'])
    extended_shed['gmaps_address'] = gmaps_address
    return extended_shed


def scrape_and_write_shed_statuses(shed_list):
    gmaps = GoogleMaps()
    n_shed_list = len(shed_list)
    extended_shed_list = []
    for i, shed in enumerate(shed_list):
        shed_status = shed_status_scraper.scrape_shed_status(
            shed,
            i,
            n_shed_list,
        )
        extended_shed = shed | shed_status

        shed_data_3p = get_shed_data_3p(extended_shed, gmaps)
        extended_shed = extended_shed | shed_data_3p

        write_extended_shed(extended_shed)
        extended_shed_list.append(extended_shed)

    return extended_shed_list


def sort_extended_shed_list(extended_shed_list):
    return sorted(
        extended_shed_list,
        key=lambda extended_shed:
        str(extended_shed['time_last_updated_by_shed_ut'])
        + str(extended_shed['shed_id']),
    )


def write_LEGACY_shed_status_list(extended_shed_list):
    n_extended_shed_list = len(extended_shed_list)
    json_file = os.path.join(DIR_LATEST, 'shed_status_list.all.json')

    sorted_extended_shed_list = sort_extended_shed_list(
        extended_shed_list)
    JSONFile(json_file).write(sorted_extended_shed_list)
    log.info(f'Saved {n_extended_shed_list} sheds to {json_file}')


def get_extended_shed_status_files():
    extended_shed_status_files = []
    for file_only in os.listdir(DIR_LATEST):
        if file_only[:14] == 'extended_shed.' and file_only[-5:] == '.json':
            extended_shed_status_files.append(
                os.path.join(DIR_LATEST, file_only)
            )
    return extended_shed_status_files


def get_extended_shed_list():
    extended_shed_status_files = get_extended_shed_status_files()
    extended_shed_list = []
    for extended_shed_status_file in extended_shed_status_files:
        extended_shed = JSONFile(extended_shed_status_file).read()
        extended_shed_list.append(extended_shed)
    return extended_shed_list


def write_extended_shed_list():
    extended_shed_list = get_extended_shed_list()
    n_extended_shed_list = len(extended_shed_list)

    sorted_extended_shed_list = sort_extended_shed_list(
        extended_shed_list)
    json_file = os.path.join(DIR_LATEST, 'extended_shed_list.json')
    JSONFile(json_file).write(sorted_extended_shed_list)
    log.info(f'Wrote {n_extended_shed_list} extended sheds to {json_file}')


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


def filter_by_time(shed):
    time_last_updated_by_shed_ut = shed['time_last_updated_by_shed_ut']
    if not time_last_updated_by_shed_ut:
        return False
    delta_t = timex.get_unixtime() - time_last_updated_by_shed_ut
    return delta_t < MAX_UPDATE_DELAY_H * timex.SECONDS_IN.HOUR


def run_pipeline(
    do_write_LEGACY_shed_status_list=True,
    do_backpopulate=True,
    do_test=True,
):
    log.info(f'run_pipeline: {do_test=}, {do_backpopulate=},'
             + f' {do_write_LEGACY_shed_status_list=}')

    git = Git(GIT_REPO_URL)
    git.clone(DIR_DATA, force=True)
    git.checkout('data')

    shed_list = scrape_sheds()

    if do_backpopulate:
        filtered_shed_list = shed_list
        log.info('[do_backpopulate] no filter')
    else:
        filtered_shed_list = list(filter(filter_by_time, shed_list))
        n_shed_list = len(shed_list)
        n_filtered_shed_list = len(filtered_shed_list)
        log.info(
            f'Filtered {n_filtered_shed_list}/{n_shed_list} sheds,'
            + f' updated in the last {MAX_UPDATE_DELAY_H} hours',
        )

    if do_test:
        filtered_shed_list = filtered_shed_list[:10]
        log.info('[do_test] processing only 10 sheds')

    extended_shed_list = scrape_and_write_shed_statuses(filtered_shed_list)

    if do_write_LEGACY_shed_status_list:
        log.info('[do_write_LEGACY_shed_status_list]')
        write_LEGACY_shed_status_list(extended_shed_list)

    write_extended_shed_list()

    time_id = copy_latest_to_history()
    write_readme(shed_list, time_id)
