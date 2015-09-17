import sys
import ello
import delphi
import shutil

shutil.copyfile('Ello.cfg.debug', 'Ello.cfg')

ello.gera_arquivo_resource()
delphi.resource_compile("Ello.rc", "Ello.res")

if len(sys.argv)>1:
    if sys.argv[1]=='all':
        delphi.build_project("Ello.dpr")
else:
    delphi.compile_project("Ello.dpr")

