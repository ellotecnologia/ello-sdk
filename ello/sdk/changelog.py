# encoding: utf8
from __future__ import unicode_literals
from __future__ import print_function

import os
import sys
import subprocess
import shutil
import re
import logging
from datetime import datetime

from .git import git, get_changes_from, create_version_tag, push_tags
from .text_manipulation import preprocess_commit_messages

logger = logging.getLogger()

CHANGELOG_FILE = 'CHANGELOG.txt'
TMP_CHANGELOG_FILE = os.environ.get('TEMP') + '\\ell_changelog.tmp'


def make_changelog(metadata):
    logger.info("Atualizando CHANGELOG.txt")

    if not os.path.isfile(CHANGELOG_FILE):
        touch_file(CHANGELOG_FILE)

    previous_version = get_previous_version(metadata.version)
    new_version = metadata.version

    changes = get_changes_from(previous_version)
    changes = preprocess_commit_messages(changes)
    generate_temp_changelog(new_version, changes)

    merge_temp_with_changelog()

    # Atualiza informações no repositório
    commit_changelog(new_version)
    create_version_tag(new_version)
    push_tags()


def commit_changelog(version):
    logger.info("Criando commit de atualização de versão...")
    git('add ' + CHANGELOG_FILE)
    git('commit -am "Atualização do changelog ({0})" '.format(version))


def get_previous_version(version):
    version_list = version.split('.')
    previous_build_number = int(version_list[-1], 10) - 1
    version_list[-1] = str(previous_build_number)
    return '.'.join(version_list)


def generate_temp_changelog(version, changes):
    current_date = datetime.now().strftime("%d/%m/%Y")
    headline = "{} - Revisão {}\n".format(current_date, version)
    with open(TMP_CHANGELOG_FILE, 'w') as f:
        f.write(headline.encode('latin1'))
        f.write("\n")
        for line in changes:
            f.write(line.encode('latin1'))
            f.write("\n")
        f.write("\n")


def merge_temp_with_changelog():
    filenames = [TMP_CHANGELOG_FILE, CHANGELOG_FILE]
    with open('result.txt', 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)
    shutil.copyfile('result.txt', 'CHANGELOG.txt')
    os.remove('result.txt')


def touch_file(fname):
    with open(fname, 'a'):
        os.utime(fname, None)


if __name__=='__main__':
    pass
