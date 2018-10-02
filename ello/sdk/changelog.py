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

import ello.sdk.git as git

logger = logging.getLogger()

TMP_CHANGELOG_FILE = os.environ.get('TEMP') + '\\ell_changelog.tmp'


def make_changelog(metadata):
    logger.info("Updating CHANGELOG.txt")
    previous_version = get_previous_version(metadata.version)
    new_version = metadata.version

    changes = git.get_changes_from(previous_version)
    generate_temp_changelog(new_version, changes)

    edit_temp_changelog(TMP_CHANGELOG_FILE)
    merge_temp_with_changelog()

    git.commit_changelog(new_version)
    git.create_version_tag(new_version)
    git.push_tags()


def get_previous_version(version):
    version_list = version.split('.')
    previous_build_number = int(version_list[-1], 10) - 1
    version_list[-1] = str(previous_build_number)
    return '.'.join(version_list)


def generate_temp_changelog(version, changes):
    current_date = datetime.now().strftime("%d/%m/%Y")
    headline = u"{} - Revisão {}\n".format(current_date, version)
    with open(TMP_CHANGELOG_FILE, 'w') as f:
        f.write(headline.encode('latin1'))
        f.write("\n")
        for line in changes:
            line = line.decode('utf8')
            if ignore_line(line):
                continue
            line = apply_some_fixups(line)
            f.write(line.encode('latin1'))
            f.write("\n")
        f.write("\n")


def ignore_line(line):
    """ Retorna True caso a linha possua alguma das palavras definidas
    """
    return re.search('(thread|metadado|refatora..o|unit)', line)


def apply_some_fixups(line):
    # Ajusta o texto para ficar menos pessoal
    line = re.sub('- adicionei', '- Adicionado', line, flags=re.I)
    line = re.sub('- criei', '- Criado', line, flags=re.I)
    line = re.sub('(\w|\d)\(#', '\\1 (#', line)
    return line

    
def edit_temp_changelog(filename):
    notepad = subprocess.Popen(['notepad', filename])
    notepad.wait()


def merge_temp_with_changelog():
    filenames = [TMP_CHANGELOG_FILE, 'CHANGELOG.txt']
    with open('result.txt', 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)
    shutil.copyfile('result.txt', 'CHANGELOG.txt')
    os.remove('result.txt')


if __name__=='__main__':
    update_changelog_file()

