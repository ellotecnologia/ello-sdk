# coding: utf8
import os
from ello import versao_no_changelog

def cria_tag_versao():
    print u'Criando tag da versão...'
    versao = '.'.join(versao_no_changelog())
    os.system("git tag {0}".format(versao))
    os.system("git push --tags")


