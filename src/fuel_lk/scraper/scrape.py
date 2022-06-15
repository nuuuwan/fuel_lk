from fuel_lk.common import log
from fuel_lk.core import districts


def scrape_shed_data_for_single_district(
        district_id,
        province_fuel_id,
        district_fuel_id):
    log.debug(f'Scraping {district_id=}...')


def scrape_shed_data():
    expanded_district_list = districts.get_expanded_district_list()

    for expanded_district in expanded_district_list:
        scrape_shed_data_for_single_district(
            expanded_district['district_id'],
            expanded_district['district_fuel_id'],
            expanded_district['province_fuel_id'],
        )


if __name__ == '__main__':
    scrape_shed_data()
