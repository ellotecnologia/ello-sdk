import os
import sys
import subprocess
import shutil
import re
import logging

from argparse import ArgumentParser, Namespace
from datetime import datetime

from .git import git, get_changes_from, create_version_tag, push_tags, get_last_tag
from .text_manipulation import preprocess_commit_messages
from ello.project import ProjectMetadata
from ello.chamados import fecha_chamados_por_mensagem_commit

logger = logging.getLogger()

CHANGELOG_FILE = 'CHANGELOG.txt'
TMP_CHANGELOG_FILE = os.environ.get('TEMP') + '\\ell_changelog.tmp'


def init_args(parser: ArgumentParser):
    cmd = parser.add_parser('make-changelog', aliases=['mc'], help='Atualiza o arquivo de changelog')
    cmd.add_argument('--commit', help='Faz o commit das modificações do changelog no repositório', action='store_true')
    cmd.add_argument('--create-tag', help='Cria tag de versão', action='store_true')
    cmd.add_argument('--push', help='Fazer push do changelog', action='store_true')
    cmd.add_argument('--project', nargs='?', help='Caminho do arquivo .dpr')
    cmd.add_argument('--fecha-chamados', help='Fecha chamados de acordo com o número informado na msg do commit', action='store_true')
    cmd.set_defaults(func=make_changelog)


def make_changelog(args: Namespace):
    project = ProjectMetadata(args.project)

    changelog_filename = os.path.join(project.path, CHANGELOG_FILE)
    if not os.path.isfile(changelog_filename):
        return

    logger.info(f'Atualizando {os.path.relpath(changelog_filename)}')

    changes = get_changes_from(project.previous_version, os.path.relpath(project.path))
    changes = preprocess_commit_messages(changes)
    generate_temp_changelog(project.version, changes)

    merge_temp_with_changelog(changelog_filename)
    
    for p in project.dependent_projects:
        ns = Namespace(project=os.path.join(project.path, p), commit=False, push=False, fecha_chamados=False)
        make_changelog(ns)

    if args.commit:
        commit_changelog(project.version)
    
    if args.push:
        if push_tags() != 0:
            raise Exception('Falha ao fazer push da atualização do changelog')
        elif args.create_tag:
            create_version_tag(project)

    if args.fecha_chamados:
        fecha_chamados_por_mensagem_commit(changes, project.version)


def commit_changelog(version):
    logger.info('Salvando atualização de versão no repositório...')
    git('add **' + CHANGELOG_FILE)
    git('commit -am "Revisão {0}" '.format(version))


def generate_temp_changelog(version, changes):
    current_date = datetime.now().strftime('%d/%m/%Y')
    headline = '{} - Revisão {}\n'.format(current_date, version)
    with open(TMP_CHANGELOG_FILE, 'w', encoding='latin1') as f:
        f.write(headline)
        f.write('\n')
        for line in changes:
            # As instruções de codificação são para corrigir caracteres que não são
            # aceitos no encoding Latin-1
            f.write(line.encode('latin1', errors='replace').decode('latin1'))
            f.write('\n')
        f.write('\n')


def merge_temp_with_changelog(changelog_filename):
    filenames = [TMP_CHANGELOG_FILE, changelog_filename]
    with open('result.txt', 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)
    shutil.copyfile('result.txt', changelog_filename)
    os.remove('result.txt')
