import os
import subprocess
import logging

from os import path
from argparse import ArgumentParser, Namespace

from ello.project import ProjectMetadata
from ello.sdk.git import git, get_changes_from
from ello.sdk.version import bump_version
from ello.sdk.changelog import make_changelog
from ello.chamados import fecha_chamados_por_mensagem_commit

logger = logging.getLogger()


def init_args(parser: ArgumentParser) -> None:
    cmd = parser.add_parser("deploy", help="Realiza o deploy do projeto atual")
    #cmd.add_argument("--release", help="Realiza o upload da revisão", action='store_false')
    cmd.set_defaults(func=deploy)


def deploy(args: Namespace) -> None:
    project = ProjectMetadata()

    args.project = project.project_name

    changes = get_changes_from(project.previous_version, path.relpath(project.path))
    
    bump_version(project)
    make_changelog(project, changes, args)

    _commit_changelog(project.version)
    _create_version_tag(project)
    _create_version_tag(ProjectMetadata(project.dependent_projects[0])) # PDV + Gollum

    _push_new_commits()
    run_deploy_target(project)

    fecha_chamados_por_mensagem_commit(changes, project.version)


def run_deploy_target(project: ProjectMetadata) -> None:
    if not path.exists(project.makefile):
        return

    cur_dir = os.getcwd()
    os.chdir(project.path)
    subprocess.call("make deploy")
    os.chdir(cur_dir)

    for p in project.dependent_projects:
        deploy(Namespace(project=path.join(project.path, p)))
    

def _commit_changelog(version):
    logger.info('Salvando atualização de versão no repositório...')
    git('add ** CHANGELOG.txt')
    git('commit -am "Revisão {0}" '.format(version))


def _create_version_tag(project: ProjectMetadata):
    if project.tag_prefix:
        tag_name = project.tag_prefix + project.version
    else:
        tag_name = project.version
    logger.info("Criando tag {}".format(tag_name))
    git("tag {0}".format(tag_name))


def _push_new_commits():
    logger.info("Enviando atualizações para o repositório remoto (commits, tags)...")
    exit_code = git("push")
    if exit_code == 0:
        exit_code = git("push --tags")
    if exit_code != 0:
        raise Exception('Falha ao fazer push do novo release')
