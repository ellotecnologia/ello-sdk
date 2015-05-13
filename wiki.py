#coding: utf8
from dokuwikixmlrpc import DokuWikiClient
import ello
import config

WIKI_URL = 'http://wiki.ellotecnologia.net.br'
SITE_URL = 'http://www.ellotecnologia.net.br '

def atualiza_pagina_downloads(wiki, versao):
    print 'Atualizando links de download do wiki... (%s)' % versao
    revisao = versao
    build   = versao.split('.')[-1]
    versao  = '.'.join(versao.split('.')[0:3])
    executavel = "Ello-{0}.{1}-compactado.exe".format(versao, build)

    new_page = ur'''
~~NOTOC~~

====== Downloads ======

===== Versão {versao} (revisão {revisao}) =====

  * [[{site}/versoes/{executavel}|Executável compactado]]
  * [[{site}/versoes/Update-{versao}.exe|Atualizador]]
  * [[{site}/versoes/relatorios-{versao}.7z|Relatórios]]
'''
    new_page = new_page.format(
        site=SITE_URL,
        revisao=revisao,
        build=build, 
        versao=versao, 
        executavel=executavel)
    wiki.put_page('wiki:downloads', new_page, summary='', minor='')

def atualiza_changelog(wiki):
    print 'Atualizando Changelog do wiki...'
    f = open('CHANGELOG.txt', 'r')
    new_page = u'''\
~~NOTOC~~
====== Registro de Atualizações ======
%s''' % f.read().decode('latin1')
    f.close()
    wiki.put_page('wiki:changelog', new_page, summary='', minor='')

def atualiza_wiki():
    print 'Atualizando wiki...'
    wiki = DokuWikiClient(WIKI_URL, config.wiki_user, config.wiki_password)
    versao = '.'.join(ello.versao_no_changelog())
    atualiza_pagina_downloads(wiki, versao)
    atualiza_changelog(wiki)

if __name__=="__main__":
    atualiza_wiki()

