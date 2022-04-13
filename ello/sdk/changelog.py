import os
import sys
import subprocess
import shutil
import re
import logging
from datetime import datetime

from .git import git, get_changes_from, create_version_tag, push_tags, get_last_tag
from .text_manipulation import preprocess_commit_messages
from .version import get_previous_version
from ello.project import ProjectMetadata
from ello.chamados import fecha_chamados_por_mensagem_commit

logger = logging.getLogger()

CHANGELOG_FILE = 'CHANGELOG.txt'
TMP_CHANGELOG_FILE = os.environ.get('TEMP') + '\\ell_changelog.tmp'


def init_args(parser):
    cmd = parser.add_parser('make-changelog', aliases=['mc'], help='Atualiza o arquivo de changelog')
    cmd.add_argument('--commit', help='Faz o commit das modificações do changelog no repositório', action='store_true')
    cmd.add_argument('--create-tag', help='Cria tag de versão', action='store_true')
    cmd.add_argument('--push', help='Fazer push do changelog', action='store_true')
    cmd.add_argument('--last-version', help='Última versão lançada')
    cmd.set_defaults(func=make_changelog)


def make_changelog(args):
    logger.info('Atualizando CHANGELOG.txt')

    if not os.path.isfile(CHANGELOG_FILE):
        touch_file(CHANGELOG_FILE)

    metadata = ProjectMetadata()
    if args.last_version:
        previous_version = args.last_version
    else:
        previous_version = get_previous_version(metadata)

    changes = get_changes_from(previous_version)
    changes = preprocess_commit_messages(changes)
    generate_temp_changelog(metadata.version, changes)

    merge_temp_with_changelog()

    # Atualiza informações no repositório
    if args.commit:
        commit_changelog(metadata.version)
    
    if args.create_tag:
        create_version_tag(metadata)

    fecha_chamados_por_mensagem_commit(changes, metadata.version)
    
    if args.push:
        if push_tags() != 0:
            logger.info('==> Falha ao fazer push da atualização do changelog <==')


def commit_changelog(version):
    logger.info('Salvando atualização de versão no repositório...')
    git('add ' + CHANGELOG_FILE)
    git('commit -am "Atualização do changelog ({0})" '.format(version))


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


def merge_temp_with_changelog():
    filenames = [TMP_CHANGELOG_FILE, CHANGELOG_FILE]
    with open('result.txt', 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)
    shutil.copyfile('result.txt', 'CHANGELOG.txt')
    os.remove('result.txt')


def latest_changes_text():
    """Retorna o texto da última modificação do changelog"""
    changelog_header = re.compile('\d{2}/\d{2}/\d{4} - ')
    lines = []
    with open('CHANGELOG.txt') as changelog:
        lines.append(changelog.readline())
        for line in changelog:
            match = changelog_header.search(line)
            if match:
                break
            lines.append(line)
    return ''.join(lines)


def touch_file(fname):
    with open(fname, 'a'):
        os.utime(fname, None)