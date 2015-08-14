import ello
import delphi
import shutil

shutil.copyfile('Ello.cfg.debug', 'Ello.cfg')

ello.gera_arquivo_resource()
delphi.resource_compile("Ello.rc", "Ello.res")
delphi.build_project("Ello.dpr")

