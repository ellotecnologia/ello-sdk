#coding: utf8
import sys
import wiki
import changelog
import repositorio
import notificador
import instalador
import ello
import test_pipeline

if __name__=="__main__":
    if len(sys.argv)>1:
        param = sys.argv[1]
    else:
        param = ''

    if param=='all':
        ello.build_debug()
    elif param=='deploy':
        ello.build_and_deploy()
    elif param=='sdeploy':
        ello.build_and_deploy_silently()
    elif param=='pre': # pre-release
        ello.build_and_deploy_pre_release()
    elif param=='changelog':
        ello.atualiza_changelog()
    elif param=='clean':
        ello.clean_working_dir()
    elif (param=='resources') or (param=='res'):
        ello.gera_resources()
    elif (param=='installer'):
        instalador.build_and_deploy()
    elif (param=='test') or (param=='tests'):
        test_pipeline.build_tests()
    elif param=='wiki':
        wiki.atualiza_wiki()
    elif param=='notify':
        notificador.notifica()
    else:
        ello.compile_project()

