#coding: utf8
import os
import os.path
import shutil
import subprocess

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
    build_project(project, args)
    pack_artifact(project, args)
    deploy_artifact(project, args)


def build_project(project, args):
    if os.path.isfile('scripts/build.bat'):
        call_custom_build()
        return
    # quick fix (kludge) to handle different projects
    if project.name=='ello':
        build_ello_project(project, args)
    else:
        delphi.build_project(project, args)
    #if args.build_installer:
    #    instalador.build_and_deploy()


def pack_artifact(project, args):
    if os.path.isfile('scripts/pack.bat'):
        call_custom_packer(project)
        return
    if project.name=='ello':
        project.artifact_name = build_packed_artifact(project)
    else:
        project.artifact_name = '{0}/{1}-{2}.exe'.format(project.output_folder, project.name, project.version)
        shutil.copyfile(project.output_file, project.artifact_name)


def deploy_artifact(project, args):
    deployer.deploy(project.artifact_name)
    if args.update_wiki:
        wiki.update_wiki_pages(project)
    if args.notify_deploy_action:
        notify_team(project)


def build_ello_project(project, args):
    if args.run_tests:
        run_test_pipeline()
    delphi.build_project(project, debug=False)
    signtool.sign(project.output_file)


def build_packed_artifact(project):
    package_name = "{0}\\{1}-{2}".format(project.output_folder, project.name, project.version)
    package_name = empacota(project.output_file, package_name)
    package_name = gera_sfx(package_name)
    return package_name


def call_custom_build():
    print("Executando build customizado")
    subprocess.call(os.getcwd() + '\\scripts\\build.bat')


def call_custom_packer(project):
    print("Executando packer customizado")
    artifact_name = subprocess.check_output([os.getcwd() + '\\scripts\\pack.bat', project.version]).strip()
    project.artifact_name = artifact_name


#def build_and_deploy_pre_release():
#    nome_executavel = output_folder() + "\\Ello.exe"
#    remove_dcus()
#    gera_resources()
#    delphi.build_project("Ello.dpr", debug=False)
#    signtool.sign(nome_executavel)
#    nome_pacote = empacota_executavel(nome_executavel)
#    deployer.deploy(nome_pacote, pasta_destino='/home/ftp/Downloads/beta')

