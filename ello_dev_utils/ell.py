#!/c/python27/python.exe
# encoding: utf8
from __future__ import unicode_literals

import logging
import argparse

logging.basicConfig(format='=> %(message)s', level=logging.INFO)

from ello_builder import config
from ello_builder.version_manager import bump_version
from ello_builder.changelog import make_changelog
from ello_builder.project import ProjectMetadata
from ello_builder.notifications import notify_team
from ello_builder.wiki import update_wiki_pages

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
    parser = argparse.ArgumentParser(description=u"Utilitário para build e deploy do projeto ello")
    commands = parser.add_subparsers(dest="command", help="Comandos")

    bump_version_cmd = commands.add_parser("bump-version", help=u"Incrementa a versão do projeto")
    bump_version_cmd.add_argument("project_path", nargs='?')

    make_changelog_cmd = commands.add_parser("make-changelog", help=u"Atualiza o arquivo de changelog")

    build_cmd = commands.add_parser("build", help=u"Faz o build do projeto")
    build_cmd.add_argument("build_mode", nargs='?')

    notify_cmd = commands.add_parser("notify-team", help=u"Envia notificação de lançamento de revisão para o time")

    wiki_cmd = commands.add_parser("update-wiki", help=u"Atualiza páginas do wiki")

    return parser.parse_args()


def main():
    args = parse_args()
    command = args.command

    if command == 'init':
        init_new_project()
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


if __name__ == "__main__":
    main()
