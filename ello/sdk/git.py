# encoding: utf8
import os
import subprocess
import logging

logger = logging.getLogger()

def commit_changelog(version):
    logger.info(u"Criando commit de atualização de versão...")
    with open(os.devnull, 'wb') as FNULL:
        subprocess.call(u'git commit -am "Atualização do changelog ({0})" '.format(version).encode('latin-1'), stdout=FNULL)


def create_version_tag(tag_name):
    logger.info(u"Criando tag {}".format(tag_name))
    with open(os.devnull, 'wb') as FNULL:
        subprocess.call("git tag {0}".format(tag_name), stdout=FNULL)


def push_tags():
    logger.info(u"Enviando atualizações para o repositório remoto (commits, tags)...")
    with open(os.devnull, 'wb') as FNULL:
        subprocess.call("git push", stdout=FNULL, stderr=FNULL)
        subprocess.call("git push --tags", stdout=FNULL, stderr=FNULL)


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
    return p.communicate()[0].splitlines()

