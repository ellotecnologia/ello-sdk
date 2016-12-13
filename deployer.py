#coding: utf8
import os
import subprocess
import config
from utils import temp_chdir

FNULL = open(os.devnull, 'wb')

class DeployError(Exception):
    pass

def deploy(nome_arquivo, pasta_destino=None):
    """ Envia o arquivo para o servidor
    """
    caminho_arquivo = os.path.dirname(nome_arquivo) 
    with temp_chdir(caminho_arquivo):
        envia_por_scp(nome_arquivo, pasta_destino)

def envia_por_scp(nome_arquivo, pasta_destino=None):
    print u"Enviando '{0}' para o servidor...".format(nome_arquivo),
    ssh_key_file = os.path.expanduser("~") + "\\" + config.ssh_key
    pasta_destino = pasta_destino or config.ftp_path
    nome_arquivo = os.path.basename(nome_arquivo)
    params = "scp -i {} -P {} {} {}@{}:{}".format(
        ssh_key_file,
        config.ssh_port, 
        nome_arquivo,
        config.ssh_user, 
        config.hostname, 
        pasta_destino)
    exit_code = subprocess.call(params.split(), stdout=FNULL, shell=True)
    if exit_code>0:
        raise DeployError(u'Não foi possível enviar {0} para o servidor'.format(nome_arquivo))
    print "OK"

if __name__=="__main__":
    deploy('\\ello\\testando\\teste.txt')

