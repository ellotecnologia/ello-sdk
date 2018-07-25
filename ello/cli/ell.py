#!/c/python27/python.exe
# encoding: utf8
from __future__ import unicode_literals

import logging
import argparse

logging.basicConfig(format='=> %(message)s', level=logging.INFO)

from ello.sdk import config
from ello.sdk.version import bump_version
from ello.sdk.changelog import make_changelog
from ello.sdk.wiki import update_wiki_pages
from ello.chamados import inicia_chamado
from ello.notifications import notify_team
from ello.project import ProjectMetadata, init_project, require_dependency
from ello.exportador import exporta_menus, exporta_programas

from delphi import Project
from delphi.compiler import Compiler, RELEASE_MODE, DEBUG_MODE


def build_project(metadata, build_mode):
    compiler = Compiler()
    project = Project(metadata.name)

    for resource_file in metadata.resources:
        project.add_resource(resource_file)

    if build_mode == 'stacktrace':
        project.build_mode = RELEASE_MODE
        compiler.add_option('-GD')
        compiler.add_option('-DSTACKTRACE')
    elif build_mode == 'release':
        project.build_mode = RELEASE_MODE
    else:
        project.build_mode = DEBUG_MODE
        compiler.add_option('-DDEBUG_MODE')

        project.conditionals = metadata.conditionals[RELEASE_MODE]

        compiler.build(project)


def parse_args():
    parser = argparse.ArgumentParser(description="Ferramenta auxiliar de desenvolvimento de projetos Ello")
    cmd = parser.add_subparsers(dest="command", help="Comandos")

    cmd.add_parser("init", help="Inicializa projeto")
    cmd.add_parser("require", help="Adiciona uma dependência ao projeto")

    cmd.add_parser("install-hooks", help="Instala hooks do git no projeto atual")

    cmd.add_parser("workon", help="Atualiza o status de um chamado para 'Em Andamento'") \
        .add_argument("numero_chamado", nargs="?")

    cmd.add_parser("new-cert", help="Cria um novo certificado A1 de teste")

    cmd.add_parser("make-changelog", help="Atualiza o arquivo de changelog")
    cmd.add_parser("notify-team", help="Envia notificação de lançamento de revisão para o time")
    cmd.add_parser("update-wiki", help="Atualiza páginas do wiki")

    bump_version_cmd = cmd.add_parser("bump-version", help="Incrementa a versão do projeto")
    bump_version_cmd.add_argument("project_path", nargs='?')

    cmd.add_parser("exporta-menus", help="Gera um script de menu conforme banco em uso")
    cmd.add_parser("exporta-programas", help="Gera um script dos programas cadastrados no banco de dados atual")

    #build_cmd = cmd.add_parser("build", help=u"Faz o build do projeto")
    #build_cmd.add_argument("build_mode", nargs='?')

    return parser.parse_args()


def main():
    args = parse_args()
    command = args.command

    if command == 'init':
        init_project()
    elif command == 'require':
        require_dependency()
    elif command == 'workon':
        inicia_chamado(args.numero_chamado)
    elif command == 'bump-version':
        bump_version(args.project_path)
    elif command == 'make-changelog':
        make_changelog(ProjectMetadata())
    elif command == 'notify-team':
        project = ProjectMetadata()
        notify_team(project.name)
    elif command == 'update-wiki':
        project = ProjectMetadata()
        update_wiki_pages(project.name)
    elif command == 'build':
        build_project(ProjectMetadata(), args.build_mode)
    elif command == 'exporta-menus':
        exporta_menus()
    elif command == 'exporta-programas':
        exporta_programas()


if __name__ == "__main__":
    main()
