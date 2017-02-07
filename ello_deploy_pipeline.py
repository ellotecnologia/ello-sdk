#coding: utf8
import os
import sys
import re
import glob
import shutil
import datetime
import logging

import delphi
import deployer
import repositorio
import instalador
import notificador
import wiki
import signtool
import changelog
from test_pipeline import run_test_pipeline

from ConfigParser import ConfigParser
from empacotador import empacota, gera_sfx

logger = logging.getLogger()

BUILD_INFO = """
#define OFFICIAL_BUILD_INFO 3556

STRINGTABLE
BEGIN
  OFFICIAL_BUILD_INFO, "Official Build"
END
"""

def build_and_deploy():
    """ Faz o build do projeto.

          * Empacotamento do projeto (gerar arquivo compactado)
          * Envio dos arquivos para o servidor
          * Atualização do wiki (links de download e changelog)
          * Notificar suporte
    """

    build_ello_project(debug=False)
    run_test_pipeline()

    #nome_executavel = output_folder() + "\\Ello.exe"
    #signtool.sign(nome_executavel)
    #nome_pacote = empacota_executavel(nome_executavel)
    #deployer.deploy(nome_pacote)
    #instalador.build_and_deploy()
    #wiki.atualiza_wiki()

    #if len(sys.argv)==2:
    #    notificador.notifica()

def build_and_deploy_pre_release():
    nome_executavel = output_folder() + "\\Ello.exe"
    remove_dcus()
    gera_resources()
    delphi.build_project("Ello.dpr", debug=False)
    signtool.sign(nome_executavel)
    deployer.deploy(nome_executavel, pasta_destino='/home/ftp/Downloads/beta')

def build_ello_project(debug=True):
    remove_dcus()
    gera_resources()
    if debug:
        shutil.copyfile('Ello.cfg.debug', 'Ello.cfg')
    else:
        shutil.copyfile('Ello.cfg.release', 'Ello.cfg')
    delphi.build_project("Ello.dpr", debug)

def compile_ello_project():
    shutil.copyfile('Ello.cfg.debug', 'Ello.cfg')
    gera_resources()
    delphi.compile_project("Ello.dpr")

def empacota_executavel(nome_executavel):
    versao = '.'.join(changelog.ultima_versao())
    nome_pacote = "{0}\\Ello-{1}".format(output_folder(), versao)
    nome_pacote = empacota(nome_executavel, nome_pacote)
    nome_pacote = gera_sfx(nome_pacote)
    return nome_pacote

def build_and_deploy_silently():
    """ Build e deploy silencioso
    """
    ello.build()
    deployer.deploy()

def deploy_test_version():
    gera_resources()
    delphi.build_project("Ello.dpr", True)
    logger.info(u"Enviando arquivo para a pasta de testes...")
    hora = datetime.datetime.now().strftime('%H%M%S')
    shutil.copyfile('C:/Ello/Windows/Ello.exe', '\\\\10.1.1.100\\transferencia\\Wayron\\testar\\Ello-TESTDRIVE-{}.exe'.format(hora))

def atualiza_changelog():
    changelog.update()
    gera_resources()
    versao = '.'.join(changelog.ultima_versao())
    repositorio.commita_changelog(versao)
    repositorio.cria_tag_versao(versao)

def output_folder():
    config = ConfigParser()
    config.read("Ello.dof")
    return config.get("Directories", "OutputDir")

def remove_dcus():
    map(os.remove, glob.glob("dcu/*.dcu"))

def clean_working_dir():
    os.system('del /s *.ddp')
    os.system('del /s *.dsk')
    os.system('del /s *.dcu')
    os.system('del /s *.~*')

def gera_resources():
    gera_arquivo_resource(*changelog.ultima_versao())
    delphi.resource_compile("Ello.rc", "Ello.res")
    delphi.resource_compile("extra_resources.rc", "extra_resources.res")

def gera_arquivo_resource(major, minor, build, release):
    logger.info(u"Gerando arquivo resources da versão {0}.{1}.{2}.{3}".format(major, minor, build, release))
    grava_arquivo_resource(major, minor, build, release, BUILD_INFO)
    # Remove informacoes de build para deixar o arquivo rc sem as informações de build
    grava_arquivo_resource(major, minor, build, release, '')

def grava_arquivo_resource(major, minor, build, release, build_info):
    with open(os.path.dirname(__file__)+'\\ello.rc.template', 'r') as template_file:
        template = template_file.read().decode('utf8')
    f = open('Ello.rc', 'w')
    file_content = template.format(major=major, 
                                  minor=minor, 
                                  build=build, 
                                  release=release,
                                  build_info=build_info)
    file_content = file_content.encode('latin1')
    f.write(file_content)
    f.close()

if __name__=="__main__":
    build_project(debug=True)

