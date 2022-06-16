

from fuel_lk.workflows import common_workflows

if __name__ == '__main__':
    common_workflows.run_pipeline(
        do_write_LEGACY_shed_status_list=True,
        do_backpopulate=True,
        do_test=False,
    )
