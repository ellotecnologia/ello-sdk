#coding: utf8
import os
import subprocess
import logging

def sign(nome_executavel):
    logger = logging.getLogger()
    logger.info(u"Assinando arquivo {0}".format(nome_executavel))
    FNULL = open(os.devnull, 'wb')
    caminho_certificado = "Certificado\\mycert.pfx" 
    senha_certificado = "ello3556"
    sign_tool = '"C:\\Program Files (x86)\\Windows Kits\\8.0\\bin\\x86\\signtool.exe"'
    params = '{0} sign /f {1} /p {2} {3}'.format(sign_tool, caminho_certificado, senha_certificado, nome_executavel)
    exit_code = subprocess.call(params, stdout=FNULL)
    if exit_code>0:
        raise Exception(u'Não foi possível assinar o executável')

if __name__=="__main__":
    import sys
    sign(sys.argv[1])
