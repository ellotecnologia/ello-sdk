# encoding: utf8
from __future__ import print_function
from __future__ import unicode_literals

import os
import fileinput
import logging
import subprocess

DELPHI_PATH = os.getenv('DELPHI_BIN')

class ResourceFile:

    def __init__(self, project_filename):
        resource_file = os.path.basename(project_filename).replace('.dpr', '.rc')
        resource_path = os.path.dirname(project_filename)
        self.filename = os.path.join(resource_path, resource_file)

    def update_version(self, version):
        version_split = version.split('.')
        if len(version_split) < 4:
            version_split.append('0')
        dot_version = '.'.join(version_split)
        comma_version = ','.join(version_split)

        for line in fileinput.input(self.filename, inplace=True):
            line = line.decode('utf8').rstrip()
            if 'FILEVERSION' in line:
                line = 'FILEVERSION {}'.format(comma_version)
            elif 'PRODUCTVERSION' in line:
                line = 'PRODUCTVERSION {}'.format(comma_version)
            elif 'VALUE "FileVersion"' in line:
                header, _ = line.split(',')
                line = '{}, "{}\\0"'.format(header, dot_version)
            elif 'VALUE "ProductVersion"' in line:
                header, _ = line.split(',')
                line = '{}, "{}\\0"'.format(header, dot_version)
            print(line.encode('utf8'))


def compile_resources(resource_list):
    for filename in resource_list:
        compile_resource_file(filename)


def compile_resource_file(resource_filename):
    logging.info("Compiling resource file {0}".format(resource_filename))
    output_filename = resource_filename.replace('.rc', '.res')
    params = "{0}\\brcc32 {1} -fo{2}".format(DELPHI_PATH, resource_filename, output_filename)
    with open(os.devnull, 'wb') as FNULL:
        brcc32 = subprocess.Popen(params.split(), stdout=FNULL)
        exit_code = brcc32.wait()
        if exit_code != 0:
            raise Exception('Resource compilation error')


if __name__ == "__main__":
    import sys
    resource = ResourceFile(sys.argv[1])
    resource.update_version(sys.argv[2])
