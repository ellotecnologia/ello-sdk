# encoding: utf8
from __future__ import unicode_literals

import sys
import re
import logging
from io import StringIO

import dokuwikixmlrpc

import config
from ello.sdk import git

logger = logging.getLogger()

WIKI_URL = 'http://wiki.ellotecnologia.net.br'
SITE_URL = 'http://www.ellotecnologia.net.br'

def atualiza_pagina_downloads(wiki, versao):
    logger.info('Atualizando links de download do wiki... (%s)' % versao)
    revisao = versao
    build   = versao.split('.')[-1]
    versao  = '.'.join(versao.split('.')[0:3])
    executavel = "Ello-{0}.{1}-compactado.exe".format(versao, build)

    new_page = r'''
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

def atualiza_changelog(wiki, project_name):
    logger.info('Atualizando Changelog do projeto {0} no wiki...'.format(project_name))
    new_page = create_page_contents(project_name)
    wiki.put_page('wiki:changelog:{0}'.format(project_name), new_page, summary='', minor='')

def create_page_contents(project_name):
    ticket_link = "[[http://os.ellotecnologia.net.br/chamados/\\1|#\\1]]"
    contents = StringIO()
    contents.write('~~NOTOC~~\n\n')
    contents.write('====== Registro de Atualizações - {0} ======\n\n'.format(project_name))
    contents.write('\\\\\n\n')
    with open('CHANGELOG.txt', 'r') as f:
        for line in f:
            line = line.decode('latin1')
            line = re.sub('^-', '  *', line)
            line = re.sub('#(\d+)', ticket_link, line)
            contents.write(line)
    result = contents.getvalue()
    contents.close()
    return result

def update_wiki_pages(project_name):
    logger.info('Atualizando wiki...')
    try:
        wiki = dokuwikixmlrpc.DokuWikiClient(WIKI_URL, config.wiki_user, config.wiki_password)
    except:
        logger.info('Erro ao atualizar o wiki!')
        return
    versao = '.'.join(git.get_latest_tag())
    try:
        #atualiza_pagina_downloads(wiki, versao)
        atualiza_changelog(wiki, project_name)
    except dokuwikixmlrpc.DokuWikiXMLRPCError:
        logger.info('Erro ao atualizar o wiki!')

if __name__=="__main__":
    update_wiki_pages(sys.argv[1])

