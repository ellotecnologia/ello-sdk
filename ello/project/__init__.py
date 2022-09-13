import os

from .metadata import ProjectMetadata

PACKAGE_FILE = 'package.json'

PACKAGE_TEMPLATE = """\
{{
  "name": "{}", 
  "version": "0.0.1", 
  "dependencies": {{
  }}, 
  "repos": {{
  }}
}}
"""


def init_project(args):
    """ Inicializa um projeto.
        Cria o arquivo package.json para controlar as 
        dependências e configurações do projeto
    """
    if os.path.isfile(PACKAGE_FILE):
        return

    project_name = os.path.basename(os.getcwd())
    if args.name:
        project_name = args.name

    with open(PACKAGE_FILE, 'w') as f:
        f.write(PACKAGE_TEMPLATE.format(project_name))
    print('Projeto {} inicializado'.format(project_name))


def require_dependency():
    pass
