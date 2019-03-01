# encoding: utf8
from __future__ import unicode_literals
from __future__ import print_function

import os
import subprocess
import logging

logger = logging.getLogger()


def git(args):
    with open(os.devnull, 'w') as FNULL:
        subprocess.call('git {0}'.format(args).encode('latin-1'), stdout=FNULL, stderr=subprocess.STDOUT)


def create_version_tag(tag_name):
    logger.info("Criando tag {}".format(tag_name))
    git("tag {0}".format(tag_name))


def push_tags():
    logger.info("Enviando atualizações para o repositório remoto (commits, tags)...")
    git("push")
    git("push --tags")


def get_latest_tag():
    """ Get last defined tag from git log
    """
    cmd = 'git rev-list --tags --max-count=1'
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    last_hash = p.communicate()[0].strip()

    cmd = 'git describe --tags {}'.format(last_hash)
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    return p.communicate()[0].strip()


def get_changes_from(from_tag):
    cmd = ['git', 'changelog', '--reverse', '{}..'.format(from_tag)]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    changes = p.communicate()[0].splitlines()
    changes = map(lambda text: text.decode('utf8'), changes)
    return changes