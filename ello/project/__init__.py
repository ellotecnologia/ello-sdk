# encoding: utf8
from __future__ import unicode_literals
from __future__ import print_function

import os

from .metadata import ProjectMetadata

PACKAGE_FILE = 'package.json'

PACKAGE_TEMPLATE = """\
{{
  "name": "{}", 
  "version": "0.1", 
  "dependencies": {{
  }}, 
  "repos": {{
  }}
}}
"""


def init_project():
    """ Inicializa um projeto.
        Cria o arquivo package.json para controlar as 
        dependências e configurações do projeto
    """
    if os.path.isfile(PACKAGE_FILE):
        print('Projeto já inicializado')
        return
    nome_projeto = os.path.basename(os.getcwd())
    with open(PACKAGE_FILE, 'w') as f:
        f.write(PACKAGE_TEMPLATE.format(nome_projeto))
    print('Projeto {} inicializado'.format(nome_projeto))


def require_dependency():
    pass
