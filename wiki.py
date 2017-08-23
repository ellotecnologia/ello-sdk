#coding: utf8
import re
import logging
from StringIO import StringIO

import dokuwikixmlrpc

import changelog
import config

logger = logging.getLogger()

WIKI_URL = 'http://wiki.ellotecnologia.net.br'
SITE_URL = 'http://www.ellotecnologia.net.br'

def atualiza_pagina_downloads(wiki, versao):
    logger.info('Atualizando links de download do wiki... (%s)' % versao)
    revisao = versao
    build   = versao.split('.')[-1]
    versao  = '.'.join(versao.split('.')[0:3])
    executavel = "Ello-{0}.{1}-compactado.exe".format(versao, build)

    new_page = ur'''
~~NOTOC~~

====== Downloads ======

===== Versão {versao} (revisão {revisao}) =====

  * [[{site}/downloads/{executavel}|Executável compactado]]
  * [[{site}/downloads/Update-{versao}.exe|Atualizador]]
  * [[{site}/downloads/relatorios-{versao}.zip|Relatórios]]
'''
    new_page = new_page.format(
        site=SITE_URL,
        revisao=revisao,
        build=build, 
        versao=versao, 
        executavel=executavel)
    wiki.put_page('wiki:downloads', new_page, summary='', minor='')

def atualiza_changelog(wiki):
    logger.info('Atualizando Changelog do wiki...')
    ticket_link = "[[http://os.ellotecnologia.net.br/\\1|#\\1]]"
    contents = StringIO()
    print >>contents, u'~~NOTOC~~'
    print >>contents, u'====== Registro de Atualizações - Projeto Ello ======'
    print >>contents, u'\\\\'
    with open('CHANGELOG.txt', 'r') as f:
        for line in f:
            line = line.decode('latin1')
            line = re.sub('^-', '  *', line)
            line = re.sub('#(\d+)', ticket_link, line)
            contents.write(line)
    print >>contents, u'===== Anos anteriores ====='
    print >>contents, u'  * [[changelog:ello:2013]]'
    print >>contents, u'  * [[changelog:ello:2014]]'
    print >>contents, u'  * [[changelog:ello:2015]]'
    print >>contents, u'  * [[changelog:ello:2016]]'

    new_page = contents.getvalue()
    contents.close()

    wiki.put_page('wiki:changelog:ello', new_page, summary='', minor='')

def atualiza_wiki():
    logger.info('Atualizando wiki...')
    try:
        wiki = dokuwikixmlrpc.DokuWikiClient(WIKI_URL, config.wiki_user, config.wiki_password)
    except:
        logger.info('Erro ao atualizar o wiki!')
        return
    versao = '.'.join(changelog.ultima_versao())
    try:
        atualiza_pagina_downloads(wiki, versao)
        atualiza_changelog(wiki)
    except dokuwikixmlrpc.DokuWikiXMLRPCError:
        logger.info('Erro ao atualizar o wiki!')

if __name__=="__main__":
    atualiza_wiki()

