#coding: utf8
import os
import subprocess

FNULL = open(os.devnull, 'wb')

def resource_compile(resource_filename, output_filename):
    params = "brcc32 %s -fo%s" % (resource_filename, output_filename)
    subprocess.call(params.split(), stdout=FNULL)

def compile_project(project_name):
    params = "dcc32 -W- -H- {0}".format(project_name).split()
    subprocess.call(params)

def build_project(project_filename, debug=True):
    print u"Compilando projeto %s..." % project_filename,
    if debug:
        print "Modo DEBUG ativo...",
        params = "dcc32 -$O- -$W+ -$D+ -$L+ -$Y+ -$C+ -q -b".split()
    else:
        params = "dcc32 -$O+ -$W+ -$D- -$L- -$Y- -$C- -q -b -DMOSTRARTELADELOGIN -DRELEASEMODE".split()
    params.append(project_filename)

    if debug:
        dcc32 = subprocess.Popen(params, stdout=subprocess.PIPE)
        grep = subprocess.Popen(['grep', '-i', '-v', 'componentes'], stdin=dcc32.stdout)
        exit_code = dcc32.wait()
        grep.wait()
    else:
        dcc32 = subprocess.Popen(params, stdout=FNULL)
        exit_code = dcc32.wait()

    if exit_code!=0:
        raise Exception(u'-> Erro na compilação do projeto %s' % project_filename)
    #else:
    #    print
    #    print u"Compilado com sucesso!"

