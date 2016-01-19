#coding: utf8
import os
import sys
import ello
import delphi
import deployer
import notificador
import wiki
import changelog
import shutil
import datetime
import repositorio

def build_and_deploy():
    """ Faz o build do projeto.

          * Empacotamento do projeto (gerar arquivo compactado)
          * Envio dos arquivos para o servidor
          * Atualização do wiki (links de download e changelog)
          * Notificar suporte
    """
    ello.build()
    repositorio.cria_tag_versao()
    deployer.deploy()
    wiki.atualiza_wiki()

    if len(sys.argv)==2:
        notificador.notifica()

def gera_resources():
    ello.gera_arquivo_resource()
    delphi.resource_compile("Ello.rc", "Ello.res")

def build_project():
    shutil.copyfile('Ello.cfg.debug', 'Ello.cfg')
    gera_resources()
    delphi.build_project("Ello.dpr")

def compile_project():
    shutil.copyfile('Ello.cfg.debug', 'Ello.cfg')
    gera_resources()
    delphi.compile_project("Ello.dpr")

def deploy_test_version():
    gera_resources()
    delphi.build_project("Ello.dpr", True)
    print "Enviando arquivo para a pasta de testes..."
    hora = datetime.datetime.now().strftime('%H%M%S')
    shutil.copyfile('C:/Ello/Windows/Ello.exe', '\\\\10.1.1.100\\transferencia\\Wayron\\testar\\Ello-TESTDRIVE-{}.exe'.format(hora))


def build_tests():
    import subprocess

    FNULL = open(os.devnull, 'wb')

    os.chdir('tests')
    print 'Compiling tests...'

    dcc32 = subprocess.Popen('dcc32 -DCONSOLE_TEST unit_tests'.split(), stdout=FNULL)
    exit_code = dcc32.wait()

    if exit_code>0:
        print 'Compilation error!'
        sys.exit(1)

    subprocess.call(['unit_tests.exe'])


if __name__=="__main__":
    if len(sys.argv)>1:
        param = sys.argv[1]
    else:
        param = ''

    if param=='deploy':
        build_and_deploy()
    elif param=='pre': # pre-release
        ello.build()
    elif (param=='resources') or (param=='res'):
        gera_resources()
    elif param=='wiki':
        wiki.atualiza_wiki()
    elif param=='changelog':
        changelog.update()
        ello.gera_arquivo_resource()
    elif param=='notify':
        notificador.notifica()
    elif (param=='test') or (param=='tests'):
        build_tests()
    elif param=='all':
        build_project()
    else:
        compile_project()

