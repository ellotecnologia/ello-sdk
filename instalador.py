#coding: utf8
import os
import shlex
import subprocess
import logging

import changelog
import ello_deploy_pipeline as ello
from utils import temp_chdir
from deployer import envia_por_scp

logger = logging.getLogger()

def build():
    logger.info("Compilando Instalador...")
    FNULL = open(os.devnull, 'wb')
    params = shlex.split('"\\Program Files (x86)\\Inno Setup 5\\ISCC.exe" Instalador.iss')
    with temp_chdir('/dev/ello-instalador/'):
        exit_code = subprocess.call(params, stdout=FNULL)
        if exit_code>0:
            raise DeployError(u'Erro ao compilar o instalador')

def deploy():
    versao = '.'.join(changelog.ultima_versao())
    release_path = ello.output_folder()
    filename = "Ello-Instalador-{0}.exe".format(versao)
    with temp_chdir('/dev/ello-instalador/Output'):
        envia_por_scp(filename)

def build_and_deploy():
    build()
    deploy()

if __name__=="__main__":
   build()
   deploy()

