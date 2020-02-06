import os
import logging

from ello.sdk.git import git
from ello.project.metadata import ProjectMetadata
from ello.windows.processes import delphi_is_running
#from delphi import compile_package, install_package

#PACKAGES_PATH = os.environ.get('COMPONENTES')
PACKAGES_PATH = "pkgs"

def install_dependencies(args):
    if delphi_is_running():
        logging.info('Eh necessario fechar o Delphi antes de executar esta operacao.')
        return

    metadata = ProjectMetadata()
    if not os.path.exists(PACKAGES_PATH):
        os.mkdir(PACKAGES_PATH)
    for dependency, repo, hash in metadata.dependencies():
        installed_dependency = os.path.join(PACKAGES_PATH, dependency)
        if not os.path.exists(installed_dependency):
            logging.info("Baixando pacote {}, aguarde...".format(dependency))
            git('clone {} {}'.format(repo, installed_dependency))
    #print(args)
