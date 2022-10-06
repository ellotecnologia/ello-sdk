import os
import sys
import subprocess
import shutil
import re
import logging

from typing import List
from argparse import ArgumentParser, Namespace
from datetime import datetime

from .git import get_changes_from, get_last_tag
from .text_manipulation import preprocess_commit_messages
from ello.project import ProjectMetadata

logger = logging.getLogger()

CHANGELOG_FILE = 'CHANGELOG.txt'
TMP_CHANGELOG_FILE = os.environ.get('TEMP') + '\\ell_changelog.tmp'


def init_args(parser: ArgumentParser):
    cmd = parser.add_parser('make-changelog', aliases=['mc'], help='Atualiza o arquivo de changelog')
    cmd.add_argument('--project', nargs='?', help='Caminho do arquivo .dpr')
    cmd.set_defaults(func=_make_changelog)


def _make_changelog(args: Namespace):
    project = ProjectMetadata(args.project)
    changes = get_changes_from(project.previous_version, os.path.relpath(project.path))
    make_changelog(project, changes, args)


def make_changelog(project: ProjectMetadata, changes: List[str], args: Namespace):
    changelog_filename = os.path.join(project.path, CHANGELOG_FILE)
    if not os.path.isfile(changelog_filename):
        return

    logger.info(f'Atualizando {os.path.relpath(changelog_filename)}')

    changes = preprocess_commit_messages(changes)
    generate_temp_changelog(project.version, changes)
    merge_temp_with_changelog(changelog_filename)
    
    for p in project.dependent_projects:
        ns = Namespace(project=os.path.join(project.path, p))
        _make_changelog(ns)


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
