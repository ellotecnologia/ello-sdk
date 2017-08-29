#coding: utf8
import os
import shutil

import delphi

from pipeline import deployer
from pipeline import setup_builder
from pipeline import wiki
from pipeline import signtool
from pipeline import changelog
from pipeline import git
from pipeline.packer import empacota, gera_sfx
from pipeline.notifications import notify_team
from pipeline.test_pipeline import run_test_pipeline

def build_and_deploy(project, args):
    # quick fix (kludge) to handle different projects
    if project.name.lower()=='ello':
        build_and_deploy_ello(project, args)
    else:
        build_and_deploy_other_project(project, args)

def build_and_deploy_other_project(project, args):
    delphi.build_project(project, args)
    artifact_name = project.output_folder + "\\{0}.exe".format(project)
    deploy_name = '{0}/{1}-{2}.exe'.format(project.output_folder, project.name, project.version)
    shutil.copyfile(artifact_name, deploy_name)
    deployer.deploy(deploy_name)
    if args.update_wiki:
        wiki.update_wiki_pages(project)
    if args.notify_deploy_action:
        notify_team(project)

def build_and_deploy_ello(project, args):
    if args.run_tests:
        run_test_pipeline()

    delphi.build_project(project, debug=False)

    artifact_name = project.output_folder + "\\{0}.exe".format(project)
    signtool.sign(artifact_name)
    artifact_name = build_packed_artifact(project, artifact_name)
    deployer.deploy(artifact_name)

    #if args.build_installer:
    #    instalador.build_and_deploy()
    if args.update_wiki:
        wiki.update_wiki_pages(project)
    if args.notify_deploy_action:
        notify_team(project)

def build_packed_artifact(project, executable_name):
    package_name = "{0}\\{1}-{2}".format(project.output_folder, project.name, project.version)
    package_name = empacota(executable_name, package_name)
    package_name = gera_sfx(package_name)
    return package_name

#def build_and_deploy_pre_release():
#    nome_executavel = output_folder() + "\\Ello.exe"
#    remove_dcus()
#    gera_resources()
#    delphi.build_project("Ello.dpr", debug=False)
#    signtool.sign(nome_executavel)
#    nome_pacote = empacota_executavel(nome_executavel)
#    deployer.deploy(nome_pacote, pasta_destino='/home/ftp/Downloads/beta')

