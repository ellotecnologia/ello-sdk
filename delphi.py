#coding: utf8
import os
import subprocess
import shlex

FNULL = open(os.devnull, 'wb')

DELPHI_PATH = "C:/Program Files (x86)/Borland/Delphi7/Bin/"
COMPILER_PATH = DELPHI_PATH + "dcc32.exe"

def resource_compile(resource_filename, output_filename):
    params = "{0}brcc32 {1} -fo{2}".format(DELPHI_PATH, resource_filename, output_filename)
    subprocess.call(params.split(), stdout=FNULL)

def compile_project(project_name):
    params = "{0} -W- -H- -q {1}".format(COMPILER_PATH, project_name).split()
    subprocess.call(params)

def build_project(project_filename, debug=True):
    print u"Compilando projeto {0}...".format(project_filename),
    if debug:
        print "Modo DEBUG ativo...",
        params = shlex.split("\"{0}\" -$O- -$W+ -$D+ -$L+ -$Y+ -$C+ -q -b".format(COMPILER_PATH))
    else:
        params = shlex.split("\"{0}\" -$O+ -$W- -$D- -$L- -$Y- -$C- -q -b -DMOSTRARTELADELOGIN -DRELEASEMODE".format(COMPILER_PATH))
    params.append(project_filename)

    if debug:
        dcc32 = subprocess.Popen(params, stdout=subprocess.PIPE)
        grep = subprocess.Popen(['grep', '-i', '-v', 'componentes'], stdin=dcc32.stdout, stdout=subprocess.PIPE)

        warnings = 0
        hints = 0
        for line in grep.stdout:
            if 'Warning:' in line:
                warnings += 1
            if 'Hint:' in line:
                hints += 1
            print line.rstrip()

        exit_code = dcc32.wait()
        grep.wait()

        print 'Warnings: {0} Hints: {1}'.format(warnings, hints)
    else:
        dcc32 = subprocess.Popen(params, stdout=FNULL)
        exit_code = dcc32.wait()
        print

    if exit_code!=0:
        raise Exception(u"-> Erro na compilação do projeto {0}".format(project_filename))
    #else:
    #    print
    #    print u"Compilado com sucesso!"

if __name__=="__main__":
    build_project("Ello.dpr")

