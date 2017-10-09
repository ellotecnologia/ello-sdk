# encoding: utf8
import logging
import argparse
import json
import os.path

import delphi

from pipeline import git
from pipeline import wiki
from pipeline import changelog
from pipeline import deploy_pipeline
from pipeline import test_pipeline
from pipeline.utils import clean_working_dir
from pipeline.notifications import notify_team

logging.basicConfig(format='=> %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class PackageFileNotFound(Exception):
    pass


def get_project_name():
    package_file = 'package.json'
    if not os.path.isfile(package_file):
        raise PackageFileNotFound('Package file not found')
    with open(package_file, 'r') as f:
        package = json.load(f)
    return package['name']


def parse_args():
    parser = argparse.ArgumentParser(description=u"Utilitário para build e deploy do projeto ello")
    commands = parser.add_subparsers(dest="command", help="Comandos")

    all_cmd       = commands.add_parser("all", help=u"Faz build completo do projeto")
    deploy_cmd    = commands.add_parser("deploy", help=u"Faz o build e deploy do projeto para o servidor")
    changelog_cmd = commands.add_parser("changelog", help=u"Constroi o changelog")
    clean_cmd     = commands.add_parser("clean", help=u"Limpa pasta do projeto (remove *.dcu e outros arquivos)")
    notify_cmd    = commands.add_parser("notify", help=u"Envia notificação de lançamento de revisão para o time")
    wiki_cmd      = commands.add_parser("wiki", help=u"Atualiza páginas do wiki")
    resource_cmd  = commands.add_parser("resource", help=u"Atualiza arquivo de resources")
    pre_cmd       = commands.add_parser("pre", help=u"Cria um pre-release e envia para o servidor")

    all_cmd.add_argument("--debug", type=bool, default=True, 
                         help=u"Compila com modo debug ativo")

    deploy_cmd.add_argument("--debug", type=bool, default=False,
                            help=u"Compila com modo debug ativo")
    deploy_cmd.add_argument("--ignore-installer", default=True,
                            action="store_false",
                            dest="build_installer",
                            help=u"Não faz o build do instalador")
    deploy_cmd.add_argument("--ignore-wiki", default=True,
                            action="store_false",
                            dest="update_wiki",
                            help=u"Atualizar wiki no servidor")
    deploy_cmd.add_argument("--ignore-tests", default=True,
                            action="store_false",
                            dest="run_tests",
                            help=u"Ignora a execução da suite de testes")
    deploy_cmd.add_argument("--no-notification", default=True,
                            action="store_false",
                            dest="notify_deploy_action",
                            help=u"Notificar sobre o deploy")

    return parser.parse_args()


def main():
    args = parse_args()
    command = args.command
    project = delphi.DelphiProject(get_project_name())

    if command == 'all':
        delphi.build_project(project, args)
    elif command == 'deploy':
        deploy_pipeline.build_and_deploy(project, args)
    elif command == 'changelog':
        changelog.update_changelog(project)
    elif command == 'clean':
        clean_working_dir()
    elif command == 'resource':
        last_tag = git.get_latest_tag().split('.')
        delphi.rc_file.update_resource_file(project, *last_tag)
    elif command == 'wiki':
        wiki.update_wiki_pages(project)
    elif command == 'notify':
        notify_team(project)


if __name__ == "__main__":
    try:
        main()
    except delphi.BuildError:
        logger.info(u'Erro na compilação do projeto!')
    except test_pipeline.IntegrationTestError, e:
        logger.info(e.message)
