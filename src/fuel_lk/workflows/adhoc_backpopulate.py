
from utils import GoogleMaps, JSONFile

from fuel_lk.base import Git
from fuel_lk.common import DIR_DATA, GIT_REPO_URL
from fuel_lk.workflows import common_workflows

if __name__ == '__main__':
    git = Git(GIT_REPO_URL)
    git.clone(DIR_DATA, force=True)
    git.checkout('data')

    gmaps = GoogleMaps()

    legacy_json_file = common_workflows.get_legacy_json_file()

    extended_shed_list = JSONFile(legacy_json_file).read()
    for extended_shed in extended_shed_list:
        common_workflows.write_extended_shed(extended_shed)

    extended_shed_list = common_workflows.get_extended_shed_list()
    for extended_shed in extended_shed_list:
        shed_data_3p = common_workflows.get_shed_data_3p(extended_shed, gmaps)
        extended_shed = extended_shed | shed_data_3p

        common_workflows.write_extended_shed(extended_shed)

    common_workflows.write_extended_shed_list()

    git.add_and_commit('[cheat_packpopulate] Added files')
