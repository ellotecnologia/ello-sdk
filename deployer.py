#coding: utf8
import os
import subprocess
import config
from utils import temp_chdir

FNULL = open(os.devnull, 'wb')

class DeployError(Exception):
    pass

def deploy(nome_arquivo, pasta_destino=None, empacotar=True):
    """ Envia o arquivo para o servidor
    """
    caminho_arquivo = os.path.dirname(nome_arquivo) 
    with temp_chdir(caminho_arquivo):
        if empacotar:
            nome_arquivo = empacota(nome_arquivo, caminho_arquivo)
            nome_arquivo = gera_sfx(nome_arquivo)
        envia_por_scp(nome_arquivo, pasta_destino)

def empacota(nome_arquivo, caminho_arquivo):
    nome_arquivo_compactado = "{0}.7z".format(extrai_nome_arquivo(nome_arquivo))
    print "Gerando arquivo {0}".format(nome_arquivo_compactado)
    params = "7za a -bd {0} {1}".format(nome_arquivo_compactado, nome_arquivo).split()
    exit_code = subprocess.call(params, stdout=FNULL)
    if exit_code>0:
        raise DeployError(u'Não foi possível compactar arquivo {0}\\{1}'.format(caminho_arquivo, nome_arquivo))
    return nome_arquivo_compactado

def gera_sfx(nome_arquivo):
    print "Gerando arquivo SFX...",
    path = os.path.dirname(os.path.abspath(__file__))
    sfx_path = path + "\\sfx\\7z.sfx"
    nome_arquivo_compactado = "{0}-compactado.exe".format(extrai_nome_arquivo(nome_arquivo))
    params = "copy /b {0} + {1} {2}".format(sfx_path, nome_arquivo, nome_arquivo_compactado)
    exit_code = subprocess.call(params, stdout=FNULL, shell=True)
    if exit_code>0:
        raise DeployError(u'Não foi possível gerar arquivo sfx')
    print "OK!"
    return nome_arquivo_compactado

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

def extrai_nome_arquivo(nome_arquivo):
    return os.path.splitext(nome_arquivo)[0]

if __name__=="__main__":
    deploy('\\ello\\testando\\teste.txt')

