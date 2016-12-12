# coding: utf8
import subprocess

def cria_tag_versao(versao):
    print u"Criando tag da versão..."
    subprocess.call("git tag {0}".format(versao))
    subprocess.call("git push --tags")

def commita_changelog(versao):
    print u"Criando commit de atualização de versão..."
    subprocess.call(u'git commit -am "Atualização do changelog ({0})" '.format(versao).encode('latin-1'))

