from gig import ents
from gig.ent_types import ENTITY_TYPE
from utils import CSVFile


def get_expanded_district_list():
    district_list = ents.get_entities(ENTITY_TYPE.DISTRICT)
    district_fuel_info_list = CSVFile(
        'src/fuel_lk/data/districts.fuel.csv').read()
    district_fuel_info_idx = dict(list(map(
        lambda d: [d['name'], d],
        district_fuel_info_list,
    )))

    expanded_district_list = []
    for district in district_list:
        district_fuel_info = district_fuel_info_idx[district['name']]
        district['province_fuel_id'] = district_fuel_info['province_fuel_id']
        district['district_fuel_id'] = district_fuel_info['district_fuel_id']
        expanded_district_list.append(district)
    return expanded_district_list


if __name__ == '__main__':
    print(get_expanded_district_list())
