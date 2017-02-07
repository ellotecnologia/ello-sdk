# coding: utf8
import os
import subprocess
import logging

logger = logging.getLogger()

def cria_tag_versao(versao):
    with open(os.devnull, 'wb') as FNULL:
        logger.info(u"Criando tag da versão...")
        subprocess.call("git tag {0}".format(versao), stdout=FNULL)
        logger.info(u"Fazendo o push da nova tag...")
        subprocess.call("git push --tags", stdout=FNULL, stderr=FNULL)

def commita_changelog(versao):
    logger.info(u"Criando commit de atualização de versão...")
    with open(os.devnull, 'wb') as FNULL:
        subprocess.call(u'git commit -am "Atualização do changelog ({0})" '.format(versao).encode('latin-1'), stdout=FNULL)
        subprocess.call("git push", stdout=FNULL, stderr=FNULL)

