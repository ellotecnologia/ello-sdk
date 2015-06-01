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
    elif param=='project':
        delphi.build_project("Ello.dpr")
    elif (param=='resources') or (param=='res'):
        ello.gera_arquivo_resource()
        delphi.resource_compile("Ello.rc", "Ello.res")
    elif param=='wiki':
        wiki.atualiza_wiki()
    else:
        delphi.build_project("Ello.dpr")

