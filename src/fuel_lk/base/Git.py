import os
import shutil

from utils import logx

log = logx.get_logger('Git')


class Git:
    def __init__(self, git_repo_url):
        self.git_repo_url = git_repo_url
        self.repo_name = os.path.basename(git_repo_url)
        self.dir_repo = None
        self.branch_name = None

    @property
    def cmd_clone(self):
        assert(self.git_repo_url is not None)
        assert(self.dir_repo is not None)
        return f'git clone {self.git_repo_url} {self.dir_repo}'

    @property
    def cmd_cd(self):
        assert(self.dir_repo is not None)
        return f'cd {self.dir_repo}'

    @property
    def cmd_checkout(self):
        assert(self.branch_name is not None)
        return f'git checkout {self.branch_name}'

    @property
    def cmd_git_push(self):
        assert(self.branch_name is not None)
        return f'git push origin {self.branch_name}'

    @staticmethod
    def run(*cmd_list):
        cmd = ' && '.join(cmd_list)
        log.debug(f'Running {cmd}')
        os.system(cmd)

    def init_dir_repo(self):
        if os.path.exists(self.dir_repo):
            shutil.rmtree(self.dir_repo)
        os.mkdir(self.dir_repo)

    def clone(self, dir_repo, force=False):
        self.dir_repo = dir_repo

        if not os.path.exists(self.dir_repo) or force:
            self.init_dir_repo()
            Git.run(
                self.cmd_cd,
                self.cmd_clone,
            )
        else:
            log.debug(f'{self.dir_repo} exists. Not cloning!')

    def checkout(self, branch_name):
        self.branch_name = branch_name
        Git.run(
            self.cmd_cd,
            self.cmd_checkout,
        )

    def add_all_and_commit(self, message):
        Git.run(
            'git add .',
            f'git commit -m "{message}"'
        )

    def push(self):
        Git.run(
            self.cmd_git_push
        )


# if __name__ == '__main__':
#     git = Git('https://github.com/nuuuwan/fuel_lk')
#     git.clone('/tmp/test_git.fuel_lk', force=True)
#     git.checkout('data')
