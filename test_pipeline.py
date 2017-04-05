#coding: utf8
import os
import subprocess
import logging

from utils import temp_chdir

logger = logging.getLogger()

FNULL = open(os.devnull, 'wb')

class IntegrationTestError(Exception):
    pass

def resource_compile(resource_filename, output_filename):
    logger.info("Compilando arquivo de resource: {0}".format(resource_filename))
    params = "brcc32 {0} -fo{1}".format(resource_filename, output_filename)
    subprocess.call(params.split(), stdout=FNULL)

def build_tests(project_name, description):
    logger.info(u'Compilando {0}...'.format(description))

    resource_compile('Ello.rc', project_name)

    dcc32 = subprocess.Popen('dcc32 -q -b -DMODO_CONSOLE {0}'.format(project_name).split(), stdout=FNULL)
    exit_code = dcc32.wait()

    if exit_code>0:
        raise IntegrationTestError(u'Erro ao compilar {0}!'.format(description))

def run_tests(project_name, description):
    logger.info(u'Executando {0}...'.format(description))
    with temp_chdir('/ello/windows'):
        exit_code = subprocess.call(['{0}.exe'.format(project_name)])
    if exit_code>0:
        raise IntegrationTestError(u'Falha na execução dos {0}!'.format(description))
    logger.info(u'Testes ok!')

def run_test_pipeline():
    build_tests('TestesIntegracao', u'testes de integração')
    run_tests('TestesIntegracao', u'testes de integração')

    build_tests('TestesAceitacao', u'testes de aceitação')
    run_tests('TestesAceitacao', u'testes de aceitação')

