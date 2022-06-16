import os

from fuel_lk.base import Git
from fuel_lk.common import DIR_DATA, GIT_REPO_URL
from fuel_lk.workflows.common_workflows import DIR_LATEST

if __name__ == '__main__':
    git = Git(GIT_REPO_URL)
    git.clone(DIR_DATA, force=True)
    git.checkout('data')

    legacy_json_file = os.path.join(DIR_LATEST, 'shed_status_list.all.json')
    new_json_file = os.path.join(DIR_LATEST, 'extended_status_list.json')

    os.system(f'cp {legacy_json_file} {new_json_file}')
    git.add_all_and_commit('[cheat_packpopulate] Added files')
    git.push()
