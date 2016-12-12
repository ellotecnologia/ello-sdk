#coding: utf8
import os
import subprocess
import ello
import shlex
from utils import temp_chdir
from deployer import envia_por_scp

def build():
    print "Compilando Instalador...",
    FNULL = open(os.devnull, 'wb')
    params = shlex.split('"\\Program Files (x86)\\Inno Setup 5\\ISCC.exe" Instalador.iss')
    with temp_chdir('/dev/ello-instalador/'):
        exit_code = subprocess.call(params, stdout=FNULL)
        if exit_code>0:
            raise DeployError(u'Erro ao compilar o instalador')
    print "OK"

def deploy():
    versao = '.'.join(ello.versao_no_changelog())
    release_path = ello.output_folder()
    filename = "Setup-{0}.exe".format(versao)
    with temp_chdir('/dev/ello-instalador/Output'):
        envia_por_scp(filename)

def build_and_deploy():
    build()
    deploy()

if __name__=="__main__":
   build()
   deploy()

