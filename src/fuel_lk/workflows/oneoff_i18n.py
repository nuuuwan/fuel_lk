
from utils import GoogleMaps, JSONFile, File

from fuel_lk.base import Git
from fuel_lk.common import DIR_DATA, GIT_REPO_URL, log
from fuel_lk.workflows import common_workflows

def clean_word(x):
    return x.strip()

if __name__ == '__main__':
    git = Git(GIT_REPO_URL)
    git.clone(DIR_DATA, force=False)
    git.checkout('data')

    extended_shed_list = common_workflows.get_extended_shed_list()
    words = []
    for extended_shed in extended_shed_list:
        words += [
            extended_shed['shed_name'],
            extended_shed['address'],
        ]

        if 'gmaps_address' in extended_shed:
            words.append(gmaps_address['gmaps_address'])

        for dispatch_schedule in extended_shed['dispatch_schedule_list']:
            words.append(dispatch_schedule['plant_name'])

    words = list(map(
        clean_word,
        words,
    ))

    words = sorted(list(set(words)))
    n_words = len(words)
    source_file = '/tmp/DICTIONARY.english.txt'
    File(source_file).write('\n'.join(words))
    log.info(f'Wrote {n_words} to {source_file}')
