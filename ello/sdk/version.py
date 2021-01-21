import os
import logging
import fileinput
import re
import sys
import datetime

from ello.project import ProjectMetadata
from delphi.resource import ResourceFile
from .git import get_sorted_tags


def bump_version(args):
    """ Incrementa a versão do projeto """
    project = ProjectMetadata('package.json')
    previous_version = get_previous_version(project)
    args.version = increment_version(project, previous_version)
    set_version(args)


def increment_version(project, previous_version):
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
    

def get_next_version(current_version):
    """ Incrementa o número do release da versão """
    breakpoint()
    version_list = current_version.split('.')
    next_build_number = int(version_list[-1], 10) + 1
    version_list[-1] = str(next_build_number)
    return '.'.join(version_list)

    
def get_previous_version(project):
    """ Obtém a última versão 'taggeada' do projeto.
        Leva em consideração se a versão no projeto utiliza 
        prefixo (ex: nome_projeto/1.2.3.4) ou não (ex: 1.2.3.4).
    """
    tags = get_sorted_tags()
    if project.tag_prefix:
        tags = filter(lambda t: t.startswith(project.tag_prefix), tags)
    else:
        tags = filter(lambda t: '/' not in t, tags)
    return list(tags)[-1]
    

def update_makefile_version(new_version):
    for line in fileinput.input('Makefile', inplace=True):
        match = re.search('^VERSION', line)
        if match:
            sys.stdout.write("VERSION = {0}\n".format(new_version))
        else:
            sys.stdout.write(line)


def set_version(args):
    """ Define a versao do projeto """
    project = ProjectMetadata('package.json')
    new_version = args.version
    
    logging.info('Atualizando versão do projeto {} para {}'.format(project.name, new_version))

    # Incrementa a versão do resource file caso houver algum na raiz do projeto
    resource_file = project.name + '.rc'
    if os.path.isfile(resource_file):
       resource = ResourceFile(resource_file)
       resource.update_version(new_version)

    # Incrementa a versão do resource file caso houver algum na pasta 'res'
    resource_file = 'res\\' + project.name + '.rc'
    if os.path.isfile(resource_file):
       resource = ResourceFile(resource_file)
       resource.update_version(new_version)

    # Incrementa a versão do resource file caso houver algum na pasta 'resources'
    resource_file = 'resources\\' + project.name + '.rc'
    if os.path.isfile(resource_file):
       resource = ResourceFile(resource_file)
       resource.update_version(new_version)

    # Incrementa versão do arquivo DOF do projeto delphi
    project.update_version(new_version)

    # Incrementa a versão no Makefile
    if os.path.isfile('Makefile'):
        update_makefile_version(new_version)


if __name__ == '__main__':
    project = ProjectMetadata('package.json')
    previous_version = get_previous_version(project)
    print(increment_version(project, previous_version))
