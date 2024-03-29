import sys
import logging
import argparse

logging.basicConfig(format='=> %(message)s', level=logging.INFO)

import ello.sdk.changelog
import ello.sdk.version
import ello.notifications
import ello.project.deployment

from ello.sdk import config
from ello.sdk.dependencies import install_dependencies
from ello.sdk.wiki import update_wiki_pages
from ello.sdk.git import install_hooks
from ello.sdk.database import create_new_sql_patch
from ello.chamados import inicia_chamado
from ello.project import ProjectMetadata, init_project, require_dependency
from ello.tests import update_test_project, generate_test_case

from delphi.dof import clear_dof_history
from delphi.compiler import Compiler, RELEASE_MODE, DEBUG_MODE


def main():
    parser = argparse.ArgumentParser(description="Kit de desenvolvimento Ello")
    cmd = parser.add_subparsers(dest="command", help="Comandos")

    init_cmd = cmd.add_parser("init", help="Cria estrutura de um novo projeto")
    init_cmd.add_argument("name", nargs="?")
    init_cmd.set_defaults(func=init_project)

    #cmd.add_parser("require", help="Adiciona uma dependência ao projeto")
    
    ello.project.deployment.init_args(cmd)
    ello.sdk.version.init_args(cmd)
    ello.sdk.changelog.init_args(cmd)
    ello.notifications.init_args(cmd)
    
    update_wiki_cmd = cmd.add_parser("update-wiki", help="Atualiza páginas do wiki")
    update_wiki_cmd.set_defaults(func=lambda args: update_wiki_pages(ProjectMetadata().name))    
   
    install_hooks_cmd = cmd.add_parser("install-hooks", help="Instala hooks do git no projeto atual")
    install_hooks_cmd.set_defaults(func=install_hooks)
    
    clear_dof_cmd = cmd.add_parser("clear-dof", help="Limpa o historico do arquivo .dof")
    clear_dof_cmd.set_defaults(func=lambda args: clear_dof_history(ProjectMetadata().name + ".dof"))
    
    install_cmd = cmd.add_parser("install", help="Instala dependencias do projeto")
    install_cmd.set_defaults(func=install_dependencies)
    
    sub_cmd = cmd.add_parser("update-test-project", aliases=["utp"], help="Atualiza units do projeto de Teste de acordo com o projeto testado")
    sub_cmd.add_argument("test_project_path", nargs='?', help="Caminho do arquivo .dpr")
    sub_cmd.set_defaults(func=update_test_project)

    #cmd.add_parser("workon", help="Atualiza o status de um chamado para 'Em Andamento'") \
    #    .add_argument("numero_chamado", nargs="?")

    #cmd.add_parser("new-cert", help="Cria um novo certificado A1 de teste")
    
    generate_cmd = cmd.add_parser("generate", aliases=["g"], help="Gerador de códigos")
    generate_parser = generate_cmd.add_subparsers()

    test_cmd = generate_parser.add_parser("test", help="Gera test case para a unit informada")
    test_cmd.add_argument("unit", nargs="?", help="Caminho da unit a ser testada")
    test_cmd.add_argument("dpr", nargs="?", default='', help="Caminho do projeto de testes (.dpr)")
    test_cmd.set_defaults(func=generate_test_case)
    
    patch_cmd = generate_parser.add_parser("patch", help="Gera novo patch")
    patch_cmd.set_defaults(func=create_new_sql_patch)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)
        
    args.func(args)


if __name__ == "__main__":
    main()