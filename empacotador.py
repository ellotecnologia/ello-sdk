#coding: utf8
import os
import subprocess

class ErroEmpacotamento(Exception):
    pass

FNULL = open(os.devnull, 'wb')

def empacota(nome_arquivo, nome_arquivo_gerado):
    nome_arquivo_compactado = "{0}.7z".format(nome_arquivo_gerado)
    print "Gerando arquivo {0}".format(nome_arquivo_compactado)
    params = "7za a -bd {0} {1}".format(nome_arquivo_compactado, nome_arquivo).split()
    exit_code = subprocess.call(params, stdout=FNULL)
    if exit_code>0:
        raise ErroEmpacotamento(u'Não foi possível compactar arquivo {0}'.format(nome_arquivo))
    return nome_arquivo_compactado

def gera_sfx(nome_arquivo):
    print "Gerando arquivo SFX...",
    path = os.path.dirname(os.path.abspath(__file__))
    sfx_path = path + "\\sfx\\7z.sfx"
    nome_arquivo_compactado = "{0}-compactado.exe".format(extrai_nome_arquivo(nome_arquivo))
    params = "copy /b {0} + {1} {2}".format(sfx_path, nome_arquivo, nome_arquivo_compactado)
    exit_code = subprocess.call(params, stdout=FNULL, shell=True)
    if exit_code>0:
        raise ErroEmpacotamento(u'Não foi possível gerar arquivo sfx')
    print "OK!"
    return nome_arquivo_compactado

def extrai_nome_arquivo(nome_arquivo):
    return os.path.splitext(nome_arquivo)[0]

