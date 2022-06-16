

from fuel_lk.base import Git
from fuel_lk.common import DIR_DATA, GIT_REPO_URL
from fuel_lk.workflows import common


def run_pipeline():
    git = Git(GIT_REPO_URL)
    git.clone(DIR_DATA, force=True)
    git.checkout('data')

    shed_list = common.scrape_sheds()
    extended_shed_list = common.scrape_and_write_shed_statuses(shed_list)

    # TODO: Replace
    common.write_LEGACY(extended_shed_list)

    time_id = common.copy_latest_to_history()
    common.write_readme(shed_list, time_id)


if __name__ == '__main__':
    run_pipeline()
