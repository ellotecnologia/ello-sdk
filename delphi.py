#coding: utf8
import os
import subprocess
import shlex
import logging

from termcolor import cprint

FNULL = open(os.devnull, 'wb')
DELPHI_PATH = os.getenv('DELPHI_BIN')
COMPILER_PATH = DELPHI_PATH + "\\dcc32.exe"

logger = logging.getLogger()

class BuildError(Exception):
    pass

def resource_compile(resource_filename, output_filename):
    logger.info("Compilando arquivo de resource: {0}".format(resource_filename))
    params = "{0}\\brcc32 {1} -fo{2}".format(DELPHI_PATH, resource_filename, output_filename)
    subprocess.call(params.split(), stdout=FNULL)

def compile_project(project_name):
    logger.info(u"Compilando projeto {0}...".format(project_name))
    params = "{0} -W- -H- -q {1}".format(COMPILER_PATH, project_name).split()
    exit_code = subprocess.call(params, stdout=FNULL)
    if exit_code>0:
        logger.info(u"Erro na compilação do projeto!")
    else:
        logger.info(u"Projeto compilado com sucesso!")

def build_project(project_filename, debug=True):
    if debug:
        msg = "(Modo DEBUG ativo)"
        params = shlex.split("\"{0}\" -$O- -$W+ -$D+ -$L+ -$Y+ -$C+ -q -b".format(COMPILER_PATH))
    else:
        msg = ''
        params = shlex.split("\"{0}\" -$O+ -$W- -$D- -$L- -$Y- -$C- -q -b -DRELEASEMODE".format(COMPILER_PATH))
    logger.info(u"Compilando projeto {0} {1}...".format(project_filename, msg))
    params.append(project_filename)

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
        raise BuildError(u"-> Erro na compilação do projeto {0}".format(project_filename))

if __name__=="__main__":
    build_project("Ello.dpr")

