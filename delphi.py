#coding: utf8
import os
import subprocess

FNULL = open(os.devnull, 'wb')

def resource_compile(resource_filename, output_filename):
    params = "brcc32 %s -fo%s" % (resource_filename, output_filename)
    subprocess.call(params.split(), stdout=FNULL)

def build_project(project_filename, debug=True):
    print u"Compilando projeto %s..." % project_filename,
    if debug:
        print "Modo DEBUG ativo...",
        params = "dcc32 -$O- -$W+ -$D+ -$L+ -$Y+ -$C+ -q -b".split()
    else:
        params = "dcc32 -$O+ -$W+ -$D- -$L- -$Y- -$C- -q -b".split()
    params.append(project_filename)

    dcc32 = subprocess.Popen(params, stdout=FNULL)
    exit_code = dcc32.wait()

    if exit_code!=0:
        print
        print u'-> Erro na compilação do projeto %s' % project_filename
    else:
        print u"Compilado com sucesso!"

