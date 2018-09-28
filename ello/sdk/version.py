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

    main_resource_file = 'resources\\' + project.name + '.rc'
    if not os.path.isfile(main_resource_file):
        main_resource_file = project.name + '.rc'

    logging.info('Atualizando versão do projeto {} para {}'.format(project.name, new_version))

    resource_filename = main_resource_file
    if os.path.isfile(resource_filename):
       resource = ResourceFile(resource_filename)
       resource.update_version(new_version)

    project.update_version(new_version)

    if os.path.isfile('Makefile'):
        update_makefile_version(new_version)


if __name__=="__main__":
    bump_version()
