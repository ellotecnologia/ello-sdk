#coding: utf8
import sys
import logging
import argparse

import wiki
import changelog
import notificador
import instalador
import delphi
import ello_deploy_pipeline as pipeline
import test_pipeline

logging.basicConfig(format='=> %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def parse_args():
    parser = argparse.ArgumentParser(description=u"Utilitário para build e deploy do projeto ello")
    commands = parser.add_subparsers(dest="command", help="Comandos")

    all_cmd       = commands.add_parser("all", help=u"Faz build completo do projeto")
    deploy_cmd    = commands.add_parser("deploy", help=u"Faz o build e deploy do projeto para o servidor")
    changelog_cmd = commands.add_parser("changelog", help=u"Constroi o changelog")
    clean_cmd     = commands.add_parser("clean", help=u"Limpa pasta do projeto (remove *.dcu e outros arquivos)")
    pre_cmd       = commands.add_parser("pre", help=u"Cria um pre-release e envia para o servidor")

    all_cmd.add_argument("--debug", type=bool, default=True, help=u"Compila com modo debug ativo")

    deploy_cmd.add_argument("--debug", type=bool, default=False, help=u"Compila com modo debug ativo")
    deploy_cmd.add_argument("--ignore-installer", default=True, action="store_false", dest="build_installer", help=u"Não faz o build do instalador")
    deploy_cmd.add_argument("--ignore-wiki", default=True, action="store_false", dest="update_wiki", help=u"Atualizar wiki no servidor")
    deploy_cmd.add_argument("--ignore-tests", default=True, action="store_false", dest="run_tests", help=u"Ignora a execução da suite de testes")
    deploy_cmd.add_argument("--no-notification", default=True, action="store_false", dest="notify_deploy_action", help=u"Notificar sobre o deploy")

    return parser.parse_args()

def main():
    args = parse_args()
    command = args.command

    if command=='all':
        pipeline.build_ello_project(args)
    elif command=='deploy':
        pipeline.build_and_deploy(args)
    elif command=='pre':
        pipeline.build_and_deploy_pre_release()
    elif command=='changelog':
        pipeline.atualiza_changelog()
    elif command=='clean':
        pipeline.clean_working_dir()
    #elif (param=='resources') or (param=='res'):
    #    pipeline.gera_resources()
    #elif (param=='installer'):
    #    instalador.build_and_deploy()
    elif (command=='test') or (command=='tests'):
        test_pipeline.run_test_pipeline()
    #elif param=='wiki':
    #    wiki.atualiza_wiki()
    #elif param=='notify':
    #    notificador.notifica()
    #else:
    #    pipeline.compile_ello_project()


if __name__=="__main__":
    try:
        main()
    except delphi.BuildError:
        logger.info(u'Erro na compilação do projeto!')
    except test_pipeline.IntegrationTestError, e:
        logger.info(e.message)

