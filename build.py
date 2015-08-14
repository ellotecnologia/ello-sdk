#coding: utf8
""" Faz o build do projeto.

    O processo de build é composto por:

      * Empacotamento do projeto (gerar arquivo compactado)
      * Envio dos arquivos para o servidor
      * Atualização do wiki (links de download e changelog)
      * Notificar suporte

"""

import sys
import ello
import delphi
import deployer
import notificador
import wiki
import shutil

def main():
    ello.build()
    deployer.deploy()
    #repositorio.atualiza_repositorio()
    wiki.atualiza_wiki()
    notificador.notifica()

if __name__=="__main__":
    param = sys.argv[-1]

    if param=='deploy':
        main()
    elif param=='test':
        ello.gera_arquivo_resource()
        delphi.resource_compile("Ello.rc", "Ello.res")
        delphi.build_project("Ello.dpr", False)
        shutil.copyfile('C:/Ello/Windows/Ello.exe', '\\\\10.1.1.100\\transferencia\\Wayron\\testar\\Ello-TESTDRIVE.exe')
    elif param=='project':
        delphi.build_project("Ello.dpr")
    elif (param=='resources') or (param=='res'):
        ello.gera_arquivo_resource()
        delphi.resource_compile("Ello.rc", "Ello.res")
    elif param=='wiki':
        wiki.atualiza_wiki()
    else:
        ello.gera_arquivo_resource()
        delphi.resource_compile("Ello.rc", "Ello.res")
        delphi.build_project("Ello.dpr", False)

