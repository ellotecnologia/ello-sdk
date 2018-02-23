# encoding: utf8
import os
import logging
import subprocess
import shlex
import glob
import re

from resource import compile_resources
from dof import export_cfg_file

DEBUG_MODE = 'debug'
RELEASE_MODE = 'release'

def remove_dcus():
    map(os.remove, glob.glob("dcu/*.dcu"))


class BuildError(Exception):
    pass


class Compiler(object):

    def __init__(self):
        compiler_path = os.getenv('DELPHI_BIN') + "\\dcc32.exe"
        self._params = shlex.split("\"{0}\"".format(compiler_path))

    def add_option(self, value):
        self._params.append(value)

    def build(self, project):
        self._action = 'Building'
        self._params.append("-q")
        self._params.append("-b")
        remove_dcus()
        compile_resources(project.resources)
        self._compile_project(project)

    def compile(self, project):
        self._action = 'Compiling'
        compile_resources(project.resources)
        self._compile_project(project)

    def _compile_project(self, project):
        logging.debug("Creating delphi config file")
        export_cfg_file(project.name + '.cfg', project.build_mode, project.config)

        logging.info("{} project {}".format(self._action, project.name))
        logging.debug("Compiler params: " + ' '.join(self._params))
        self._params.append(project.project_file)
        dcc32 = subprocess.Popen(self._params, stdout=subprocess.PIPE)
        output = dcc32.communicate()[0]
        exit_code = dcc32.wait()

        if exit_code!=0:
            raise BuildError("Compilation error {}".format(project.name))

        hints, warnings = self._count_hints_and_warnings(output)
        logging.info('Compilation success! Warnings: {} Hints: {}'.format(warnings, hints))

    def _count_hints_and_warnings(self, compilation_output):
        warnings = 0
        hints = 0
        for line in compilation_output.splitlines():
            if re.search('Warning:', line):
                warnings += 1
            if re.search('Hint:', line):
                hints += 1
        return hints, warnings
