import os

from utils import File, JSONFile

from fuel_lk.base import Git
from fuel_lk.common import DIR_DATA, GIT_REPO_URL, log


def clean_word(x):
    return x.strip()


if __name__ == '__main__':
    git = Git(GIT_REPO_URL)
    git.clone(DIR_DATA, force=False)
    git.checkout('data')

    base_shed_list_file = os.path.join(DIR_DATA, 'base_shed_list.json')
    base_shed_list = JSONFile(base_shed_list_file).read()

    words = []
    for base_shed in base_shed_list:
        words += [
            base_shed['shed_name'],
            base_shed['address'],
        ]

        if 'gmaps_address' in base_shed:
            words.append(base_shed['gmaps_address'])

    words = list(map(
        clean_word,
        words,
    ))

    words = sorted(list(set(words)))
    n_words = len(words)
    source_file = '/tmp/DICTIONARY.english.txt'
    File(source_file).write('\n'.join(words))
    log.info(f'Wrote {n_words} to {source_file}')
