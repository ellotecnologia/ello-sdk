#coding: utf8
import os
import subprocess
import shlex
import logging
import json
import collections
from ConfigParser import ConfigParser

from termcolor import cprint
from pipeline.utils import remove_dcus

FNULL = open(os.devnull, 'wb')
DELPHI_PATH = os.getenv('DELPHI_BIN')
COMPILER_PATH = DELPHI_PATH + "\\dcc32.exe"

logger = logging.getLogger()

class DelphiProject:

    def __init__(self, name):
        self._name = name

    def increment_version(self):
        with open('package.json', 'r') as f:
            package_info = json.load(f, object_pairs_hook=collections.OrderedDict)
        version_info = package_info['version'].split('.')
        version_info[-1] = str(int(version_info[-1]) + 1)
        package_info['version'] = '.'.join(version_info)
        with open('package.json', 'w') as f:
            f.write(json.dumps(package_info, indent=2))

    @property
    def name(self):
        return self._name.lower()

    @property
    def output_folder(self):
        config = ConfigParser()
        config.read("{0}.dof".format(self.name))
        return config.get("Directories", "OutputDir")

    @property
    def output_file(self):
        return self.output_folder + "\\{0}.exe".format(self)

    @property
    def version(self):
        with open('package.json', 'r') as f:
            package_info = json.load(f)
        return package_info['version']

    def __repr__(self):
        return self._name

    def __str__(self):
        return self._name

class BuildError(Exception):
    pass

def compile_project(project_name):
    logger.info(u"Compilando projeto {0}...".format(project_name))
    params = "{0} -W- -H- -q {1}".format(COMPILER_PATH, project_name).split()
    exit_code = subprocess.call(params, stdout=FNULL)
    if exit_code>0:
        logger.info(u"Erro na compilação do projeto!")
    else:
        logger.info(u"Projeto compilado com sucesso!")

def build_project(project, debug=True):
    remove_dcus()
    #import pdb; pdb.set_trace()
    if debug:
        msg = "(Modo DEBUG ativo)"
        params = shlex.split("\"{0}\" -$O- -$W+ -$D+ -$L+ -$Y+ -$C+ -q -b".format(COMPILER_PATH))
    else:
        msg = ''
        params = shlex.split("\"{0}\" -$O+ -$W- -$D- -$L- -$Y- -$C- -q -b -DRELEASEMODE".format(COMPILER_PATH))
    logger.info(u"Compilando projeto {0} {1}...".format(project.name, msg))
    params.append(project.name)

    if debug:
        dcc32 = subprocess.Popen(params, stdout=subprocess.PIPE)
        grep = subprocess.Popen(['grep', '-i', '-v', 'componentes'], stdin=dcc32.stdout, stdout=subprocess.PIPE)

        warnings = 0
        hints = 0

        print 
        for line_number, line in enumerate(grep.stdout):
            # ignorar as duas primeiras linhas do compilador
            if line_number<3:
                continue

            if 'Warning:' in line:
                warnings += 1
            if 'Hint:' in line:
                hints += 1
            print line.rstrip()

        exit_code = dcc32.wait()
        grep.wait()

        if (warnings>0) or (hints>0):
            cprint('Warnings: {0} Hints: {1}'.format(warnings, hints), 'red')
        else:
            cprint('Warnings: {0} Hints: {1}'.format(warnings, hints), 'green')

        print
    else:
        dcc32 = subprocess.Popen(params, stdout=subprocess.PIPE)
        output = dcc32.communicate()
        exit_code = dcc32.wait()
        if exit_code!=0:
            for line in output:
                print line

    if exit_code!=0:
        raise BuildError(u"-> Erro na compilação do projeto {0}".format(project.name))

if __name__=="__main__":
    build_project("Ello.dpr")

