

from fuel_lk.base import Git
from fuel_lk.common import DIR_DATA, GIT_REPO_URL
from fuel_lk.workflows import common_workflows


def run_pipeline():
    git = Git(GIT_REPO_URL)
    git.clone(DIR_DATA, force=True)
    git.checkout('data')

    shed_list = common_workflows.scrape_sheds()
    shed_list = shed_list[:10]
    extended_shed_list = common_workflows.scrape_and_write_shed_statuses(
        shed_list)

    # TODO: Replace
    common_workflows.write_LEGACY_shed_status_list(extended_shed_list)
    common_workflows.write_extened_status_list()

    time_id = common_workflows.copy_latest_to_history()
    common_workflows.write_readme(shed_list, time_id)


if __name__ == '__main__':
    run_pipeline()
