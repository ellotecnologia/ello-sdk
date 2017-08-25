# coding: utf8
import os
import sys
import subprocess
import shutil
import re
import logging
from datetime import datetime

from pipeline import git
from delphi.rc_file import update_resource_file

logger = logging.getLogger()

def get_next_tag():
    version_list = git.get_latest_tag().split('.')
    next_build_number = int(version_list[-1]) + 1
    version_list[-1] = str(next_build_number)
    return version_list

def generate_temp_changelog(latest_tag, changes):
    major = ".".join(latest_tag.split('.')[:-1])
    next_release = int(latest_tag.split('.')[-1], 10)+1
    next_tag = major + ".{}".format(next_release)

    data_atual = datetime.now().strftime("%d/%m/%Y")

    headline = u"{} - Revisão {}\n".format(data_atual, next_tag)

    f = open('temp.txt', 'w')
    print >>f, headline.encode('latin1')
    for line in changes:
        print >>f, line.decode('utf8').encode('latin1')
    print >>f, ""
    f.close()

def merge_temp_with_changelog():
    filenames = ['temp.txt', 'CHANGELOG.txt']
    with open('result.txt', 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)
    shutil.copyfile('result.txt', 'CHANGELOG.txt')
    os.remove('result.txt')

def get_change_list(from_tag):
    cmd = ['git', 'changelog', '--reverse', '{}..'.format(from_tag)]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    return p.communicate()[0].splitlines()

def update_changelog_file():
    logger.info("Updating CHANGELOG.txt")
    latest_tag = git.get_latest_tag()
    changes = get_change_list(latest_tag)
    generate_temp_changelog(latest_tag, changes)
    notepad = subprocess.Popen(['notepad', 'temp.txt'])
    notepad.wait()
    merge_temp_with_changelog()

def update_changelog(project_name):
    update_changelog_file()
    project_version = get_next_tag()
    update_resource_file(project_name, *project_version)
    project_version = '.'.join(project_version)
    git.commit_changelog(project_version)
    git.create_version_tag(project_version)
    git.push()

if __name__=='__main__':
    update_changelog_file()

