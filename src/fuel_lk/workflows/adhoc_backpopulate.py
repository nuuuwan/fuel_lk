import os

from utils import GoogleMaps, JSONFile

from fuel_lk.base import Git
from fuel_lk.common import DIR_DATA, GIT_REPO_URL
from fuel_lk.workflows import common_workflows
from fuel_lk.workflows.common_workflows import DIR_LATEST

if __name__ == '__main__':
    git = Git(GIT_REPO_URL)
    git.clone(DIR_DATA, force=True)
    git.checkout('data')

    gmaps = GoogleMaps()

    legacy_json_file = os.path.join(DIR_LATEST, 'shed_status_list.all.json')
    extended_shed_list = JSONFile(legacy_json_file).read()

    for extended_shed in extended_shed_list:
        common_workflows.write_extended_shed(extended_shed)

    common_workflows.write_extended_shed_list()

    git.add_and_commit('[cheat_packpopulate] Added files')
    git.push()
