#coding: utf8
import os
import subprocess
import ello
from utils import temp_chdir
import config

class DeployError(Exception):
    pass

FNULL = open(os.devnull, 'wb')

release_path = ello.output_folder()
versao = '.'.join(ello.versao_no_changelog())
executable_name = "{0}\\Ello-{1}".format(release_path, versao)

user_folder = os.path.expanduser("~")

def empacota():
    arquivo_compactado = "Ello-{0}.7z".format(versao)
    arquivo_executavel = "Ello.exe"

    print "Gerando arquivo {0}\\{1}".format(release_path, arquivo_compactado)

    params = "7za a -bd {0} {1}".format(arquivo_compactado, arquivo_executavel).split()
    exit_code = subprocess.call(params, stdout=FNULL)
    if exit_code>0:
        raise DeployError(u'Não foi possível compactar o executável')

def gera_sfx():
    path = os.path.dirname(__file__)
    sfx_path = path + "\\sfx\\7z.sfx"

    arquivo_compactado = "Ello-{0}.7z".format(versao)
    arquivo_sfx = "Ello-{0}-compactado.exe".format(versao)

    print "Gerando arquivo SFX...",

    params = "copy /b {0} + {1} {2}".format(sfx_path, arquivo_compactado, arquivo_sfx)
    exit_code = subprocess.call(params, stdout=FNULL, shell=True)
    if exit_code>0:
        raise DeployError(u'Não foi possível gerar o descompactador sfx')

    print "OK!"

def envia_para_servidor():
    print u"Enviando executável para o servidor...",
    arquivo_sfx = "Ello-{0}-compactado.exe".format(versao)
    params = "scp -i {} -P {} {} {}@{}:{}".format(
        user_folder+"\\"+config.ssh_key, 
        config.ssh_port, 
        arquivo_sfx,
        config.ssh_user, 
        config.hostname, 
        config.ftp_path)

    exit_code = subprocess.call(params.split(), stdout=FNULL, shell=True)
    if exit_code>0:
        raise DeployError(u'Não foi possível enviar o arquivo para o servidor')
    
    print "Enviado com sucesso!"

def deploy():
    """ Empacota e envia o executável para o servidor
    """
    with temp_chdir(release_path):
        empacota()
        gera_sfx()
        envia_para_servidor()

if __name__=="__main__":
    deploy()

