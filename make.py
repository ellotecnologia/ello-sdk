#coding: utf8
import sys
import logging

import wiki
import changelog
import notificador
import instalador
import delphi
import ello_deploy_pipeline as pipeline
import test_pipeline

logging.basicConfig(format='=> %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def main():
    if len(sys.argv)>1:
        param = sys.argv[1]
    else:
        param = ''

    if param=='all':
        pipeline.build_ello_project()
    elif param=='deploy':
        pipeline.build_and_deploy()
    elif param=='sdeploy':
        pipeline.build_and_deploy_silently()
    elif param=='pre': # pre-release
        pipeline.build_and_deploy_pre_release()
    elif param=='changelog':
        pipeline.atualiza_changelog()
    elif param=='clean':
        pipeline.clean_working_dir()
    elif (param=='resources') or (param=='res'):
        pipeline.gera_resources()
    elif (param=='installer'):
        instalador.build_and_deploy()
    elif (param=='test') or (param=='tests'):
        test_pipeline.run_test_pipeline()
    elif param=='wiki':
        wiki.atualiza_wiki()
    elif param=='notify':
        notificador.notifica()
    else:
        pipeline.compile_ello_project()


if __name__=="__main__":
    try:
        main()
    except delphi.BuildError:
        logger.info(u'Erro na compilação do projeto!')
    except test_pipeline.IntegrationTestError, e:
        logger.info(e.message)

