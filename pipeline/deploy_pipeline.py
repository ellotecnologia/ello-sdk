#coding: utf8
import os
import shutil

import delphi

from pipeline import deployer
from pipeline import setup_builder
from pipeline import wiki
from pipeline import signtool
from pipeline import changelog
from pipeline.packer import empacota, gera_sfx
from pipeline.notifications import notify_team
from pipeline.test_pipeline import run_test_pipeline

def build_and_deploy(project, args):
    #if args.run_tests:
    #    run_test_pipeline()

    delphi.build_project(project, args)

    artifact_name = project.output_folder + "\\{0}.exe".format(project)
    #signtool.sign(artifact_name)
    #artifact_name = empacota_executavel(artifact_name)
    #shutil.copyfile('Ello.cfg.debug', 'Ello.cfg')
    deployer.deploy(artifact_name)

    #if args.build_installer:
    #    instalador.build_and_deploy()
    if args.update_wiki:
        wiki.update_wiki_pages(project)
    if args.notify_deploy_action:
        notify_team(project)

def empacota_executavel(nome_executavel):
    versao = '.'.join(changelog.ultima_versao())
    nome_pacote = "{0}\\Ello-{1}".format(output_folder(), versao)
    nome_pacote = empacota(nome_executavel, nome_pacote)
    nome_pacote = gera_sfx(nome_pacote)
    return nome_pacote

#def build_and_deploy_pre_release():
#    nome_executavel = output_folder() + "\\Ello.exe"
#    remove_dcus()
#    gera_resources()
#    delphi.build_project("Ello.dpr", debug=False)
#    signtool.sign(nome_executavel)
#    nome_pacote = empacota_executavel(nome_executavel)
#    deployer.deploy(nome_pacote, pasta_destino='/home/ftp/Downloads/beta')

