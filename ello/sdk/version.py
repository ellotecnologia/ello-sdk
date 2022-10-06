import os
import os.path
import logging
import fileinput
import re
import sys
import datetime

from argparse import ArgumentParser, Namespace

from ello.project import ProjectMetadata
from delphi.resource import ResourceFile

def init_args(parser: ArgumentParser) -> None:
    cmd = parser.add_parser("bump-version", aliases=['bv'], help="Incrementa a versão do projeto")
    cmd.add_argument("--project", nargs='?', help="Caminho do arquivo .dpr", default='')
    cmd.set_defaults(func=_bump_version)

    cmd = parser.add_parser("set-version", help="Define versao do projeto")
    cmd.add_argument("version", help="Numero da versao")
    cmd.set_defaults(func=_set_version)
    

def _bump_version(args: ArgumentParser) -> None:
    project = ProjectMetadata(args.project)
    bump_version(project)


def _set_version(args: ArgumentParser) -> None:
    if 'project' in args:
        project = ProjectMetadata(args.project)
    else:
        project = ProjectMetadata()
    set_version(project, args.version)


def bump_version(project: ProjectMetadata) -> None:
    """ Incrementa a versão do projeto """
    new_version = increment_version(project, project.version)
    set_version(project, new_version)
    for p in project.dependent_projects:
        bump_version(ProjectMetadata(os.path.join(project.path, p)))


def set_version(project, new_version) -> None:
    """ Define a versao do projeto """
    logging.info('Atualizando {} para {}'.format(project.name, new_version))

    # Incrementa a versão do resource file caso houver algum na raiz do projeto
    resource_file = os.path.join(project.path, project.name + '.rc')
    if os.path.isfile(resource_file):
       resource = ResourceFile(resource_file)
       resource.update_version(new_version)

    # Incrementa a versão do resource file caso houver algum na pasta 'res'
    resource_file = os.path.join(project.path, 'res\\' + project.name + '.rc')
    if os.path.isfile(resource_file):
       resource = ResourceFile(resource_file)
       resource.update_version(new_version)

    # Incrementa a versão do resource file caso houver algum na pasta 'resources'
    resource_file = os.path.join(project.path, 'resources\\' + project.name + '.rc')
    if os.path.isfile(resource_file):
       resource = ResourceFile(resource_file)
       resource.update_version(new_version)

    # Incrementa versão do arquivo DOF do projeto delphi
    project.update_version(new_version)

    # Incrementa a versão no Makefile
    makefile = os.path.join(project.path, 'Makefile')
    makefile2 = os.path.join(project.path, 'Makefile_')
    if os.path.isfile(makefile):
        _update_makefile_version(makefile, new_version)
    elif os.path.isfile(makefile2):
        _update_makefile_version(makefile2, new_version)


def increment_version(project: ProjectMetadata, previous_version: str) -> str:
    """ Incrementa versão de acordo com schema de versionamento utilizado pelo projeto """
    if project.version_schema == 'calendar':
        *previous_version, last_release = previous_version.split('.')
        new_version = datetime.datetime.now().strftime('%y.%m.%d').replace('.0', '.')
        release = '0'
        if new_version == '.'.join(previous_version):
            release = str(int(last_release) + 1)
        return new_version + '.' + release
    else:
        return get_next_version(project.version)
    

def get_next_version(current_version) -> str:
    """ Incrementa o número do release da versão """
    version_list = current_version.split('.')
    next_build_number = int(version_list[-1], 10) + 1
    version_list[-1] = str(next_build_number)
    return '.'.join(version_list)

    
def _update_makefile_version(makefile, new_version):
    for line in fileinput.input(makefile, inplace=True):
        match = re.search('^VERSION', line)
        if match:
            sys.stdout.write("VERSION = {0}\n".format(new_version))
        else:
            sys.stdout.write(line)


if __name__ == '__main__':
    project = ProjectMetadata('package.json')
    previous_version = get_previous_version(project)
    print(increment_version(project, previous_version))
