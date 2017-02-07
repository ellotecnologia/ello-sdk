#coding: utf8
import os
import subprocess
import logging

logger = logging.getLogger()

FNULL = open(os.devnull, 'wb')

def build_tests():
    logger.info(u'Compilando testes de integração...')

    dcc32 = subprocess.Popen('dcc32 -q -b -DVCL -DCONSOLE_TEST TestesIntegracao'.split(), stdout=FNULL)
    exit_code = dcc32.wait()

    if exit_code>0:
        logger.info(u'Erro ao compilar testes de integração!')
        sys.exit(1)

def run_tests():
    logger.info(u'Executando testes de integração...')
    os.chdir('/ello/windows')
    exit_code = subprocess.call(['TestesIntegracao.exe'])
    if exit_code>0:
        #logger.info(u'Falha na execução dos testes de integração!')
        raise Exception(u'Falha na execução dos testes de integração!')
    logger.info(u'Testes ok!')

def run_test_pipeline():
    build_tests()
    run_tests()

