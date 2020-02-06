#!/c/Python27/python.exe
# encoding: utf8
from __future__ import unicode_literals
from __future__ import print_function

import os
import os.path
import re
import subprocess
import argparse
import json
import collections
import logging

from ello.sdk.git import git

logger = logging.getLogger()

PASTA_COMPONENTES = os.getenv('COMPONENTES')
PASTA_PROJETO_ELLO = PASTA_COMPONENTES + "\\.." 
FNULL = open(os.devnull, 'w')


def update_project_dependencies():
    """ Update current project's dependencies to reflect package.json file """
    if os.path.isfile('package.json'):
        atualiza_dependencias_package_json()
    else:
        atualiza_dependencias_modo_retrocompatibilidade()


def atualiza_dependencias_package_json():
    logger.info('Coletando metadados do projeto')
    with open('package.json', 'r') as json_file:
        package_info = json.load(json_file)
    dependencies = package_info['dependencies']
    for dependency in dependencies:
        package_name = dependency
        codigo_hash = dependencies[dependency]
        if re.match('ello', package_name, re.I):
            checkout_pacote(package_name, PASTA_PROJETO_ELLO, codigo_hash)
        else:
            checkout_pacote(package_name, PASTA_COMPONENTES, codigo_hash)


def atualiza_dependencias_modo_retrocompatibilidade():
    """ Modo de retrocompatibilidade para funcionar com revisões antigas """
    with open('LEIAME.txt', 'r') as arquivo_leiame:
        while True:
            linha = arquivo_leiame.readline()
            if not linha:
                break
            if re.match('^Excellent', linha):
                codigo_hash = extrai_hash_do_pacote(arquivo_leiame)
                checkout_pacote('excellent', PASTA_COMPONENTES, codigo_hash)
            if re.match('^ACBr', linha):
                codigo_hash = extrai_hash_do_pacote(arquivo_leiame)
                checkout_pacote('trunk2', PASTA_COMPONENTES, codigo_hash)
            if re.match('^PngComponents', linha):
                codigo_hash = extrai_hash_do_pacote(arquivo_leiame)
                checkout_pacote('PngComponents', PASTA_COMPONENTES, codigo_hash)
            if re.match('^Ello', linha):
                codigo_hash = extrai_hash_do_pacote(arquivo_leiame)
                checkout_pacote('ello', PASTA_PROJETO_ELLO, codigo_hash)


def extrai_hash_do_pacote(arquivo):
    arquivo.readline()
    return arquivo.readline().split(':')[1].strip()


def freeze_dependencies():
    """ Updates package.json file with the latest dependencies hashes """
    with open('package.json', 'r') as f:
        package_info = json.load(f, object_pairs_hook=collections.OrderedDict)

    dependencies = package_info['dependencies']
    for package_name in dependencies.iterkeys():
        package_path = PASTA_COMPONENTES
        if package_name.lower() == 'ello': # ello is not a package, it's a project
            package_path = PASTA_PROJETO_ELLO
        dependencies[package_name] = get_last_git_hash('{}\\{}'.format(package_path, package_name))

    with open('package.json', 'w') as f:
        f.write(json.dumps(package_info, indent=2))


def get_last_git_hash(repo_path):
    """ Gets the last repo hash """
    curdir = os.getcwd()
    os.chdir(repo_path)
    command = 'git log -1 --pretty=format:%H'
    git = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    out, err = git.communicate()
    os.chdir(curdir)
    return out


def checkout_pacote(nome_pacote, caminho, novo_hash):
    os.chdir("{0}/{1}".format(caminho, nome_pacote))
    if novo_hash == obtem_hash_atual():
        logger.debug("Pacote {} já está na versão correta".format(nome_pacote))
        return

    if not copia_de_trabalho_limpa():
        logger.info("Existem modificações não commitadas na pasta {0}\\{1}. Cancelando atualização.".format(caminho, nome_pacote))
        return

    logger.info('Atualizando {0} para a revisão {1}'.format(nome_pacote, novo_hash[0:7]))
    exit_code = git('checkout {0}'.format(novo_hash))
    if exit_code == 0:
        return

    logger.info("Baixando atualizações do repositório {0}".format(nome_pacote))
    git('fetch')
    git('checkout {}'.format(novo_hash))


def obtem_hash_atual():
    """ Obtem o hash do último commit no repositório atual """
    command = 'git log -1 --pretty="%H"'
    git = subprocess.Popen(command, stdout=subprocess.PIPE)
    return git.communicate()[0].strip().decode('latin1')


def copia_de_trabalho_limpa():
    return_code = subprocess.call("git diff-index --quiet HEAD --", stdout=FNULL, stderr=subprocess.STDOUT)
    return return_code==0


def main():
    logging.basicConfig(format='=> %(message)s', level=logging.INFO)
    parser = argparse.ArgumentParser(description='Gerenciador de dependencias de pacotes Ello')
    parser.add_argument('--save', action="store_true", default=False)
    args = parser.parse_args()

    if args.save:
        freeze_dependencies()
    else:
        update_project_dependencies()


if __name__ == "__main__":
    main()