# encoding: utf8
from __future__ import print_function
from __future__ import unicode_literals

import os
import logging
import fileinput
import re
import sys

from ello.project import ProjectMetadata
from delphi.resource import ResourceFile


def get_next_version(current_version):
    version_list = current_version.split('.')
    next_build_number = int(version_list[-1], 10) + 1
    version_list[-1] = str(next_build_number)
    return '.'.join(version_list)
    

def update_makefile_version(new_version):
    for line in fileinput.input('Makefile', inplace=True):
        match = re.search('^VERSION', line)
        if match:
            sys.stdout.write("VERSION = {0}\n".format(new_version))
        else:
            sys.stdout.write(line)


def bump_version():
    """ Incrementa a versão do projeto """
    metadata_filename = 'package.json'
    project = ProjectMetadata(metadata_filename)
    new_version = get_next_version(project.version)

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


if __name__ == "__main__":
    bump_version()