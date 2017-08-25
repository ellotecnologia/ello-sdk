# coding: utf8
import os
import subprocess
import logging

logger = logging.getLogger()

def create_version_tag(versao):
    with open(os.devnull, 'wb') as FNULL:
        logger.info(u"Criando tag da versão...")
        subprocess.call("git tag {0}".format(versao), stdout=FNULL)

def commit_changelog(versao):
    logger.info(u"Criando commit de atualização de versão...")
    with open(os.devnull, 'wb') as FNULL:
        subprocess.call(u'git commit -am "Atualização do changelog ({0})" '.format(versao).encode('latin-1'), stdout=FNULL)

def push():
    with open(os.devnull, 'wb') as FNULL:
        logger.info(u"Enviando atualizações para o repositório remoto (commits, tags)...")
        subprocess.call("git push", stdout=FNULL, stderr=FNULL)
        subprocess.call("git push --tags", stdout=FNULL, stderr=FNULL)

def get_latest_tag():
    """ Get last defined tag from git log
    """
    cmd = 'git describe --abbrev=0 --tags' 
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    return p.communicate()[0].strip()

