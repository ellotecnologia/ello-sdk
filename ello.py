#coding: utf8
import os
import sys
import re
import datetime
import delphi
import deployer
import glob
import instalador
import repositorio
import shutil
import wiki
import signtool
import changelog
from ConfigParser import ConfigParser

RC_FILE = u"""\
MAINICON ICON "Ello.ico"

1 VERSIONINFO
FILEVERSION {major},{minor},{build},{release}
PRODUCTVERSION {major},{minor},{build},{release}
FILEFLAGSMASK 0x3fL
#ifdef _DEBUG
 FILEFLAGS 0x9L
#else
 FILEFLAGS 0x8L
#endif
FILEOS 0x4
FILETYPE 0x1
BEGIN
    BLOCK "StringFileInfo"
    BEGIN
        BLOCK "041604E4"
        BEGIN
            VALUE "CompanyName", "Ello Tecnologia\\0"
            VALUE "FileDescription", "Sistema Ello - Automação Comercial\\0"
            VALUE "FileVersion", "{major}.{minor}.{build}.{release}\\0"
            VALUE "InternalName", "Ello\\0"
            VALUE "LegalCopyright", "Ello Tecnologia Ltda\\0"
            VALUE "LegalTrademarks", "Ello tecnologia\\0"
            VALUE "OriginalFilename", "Ello.exe\\0"
            VALUE "ProductName", "Sistema Ello\\0"
            VALUE "ProductVersion", "{major}.{minor}\\0"
            VALUE "Comments", "Sistema ERP Ello\\0"
        END
    END

    BLOCK "VarFileInfo"
    BEGIN
        VALUE "Translation", 0x0416 0x04E4
    END
END
{build_info}
"""

BUILD_INFO = """
#define OFFICIAL_BUILD_INFO 3556

STRINGTABLE
BEGIN
  OFFICIAL_BUILD_INFO, "Official Build"
END
"""

def compile_project():
    shutil.copyfile('Ello.cfg.debug', 'Ello.cfg')
    gera_resources()
    delphi.compile_project("Ello.dpr")

def build_debug():
    remove_dcus()
    shutil.copyfile('Ello.cfg.debug', 'Ello.cfg')
    gera_resources()
    delphi.build_project("Ello.dpr")

def build_and_deploy():
    """ Faz o build do projeto.

          * Empacotamento do projeto (gerar arquivo compactado)
          * Envio dos arquivos para o servidor
          * Atualização do wiki (links de download e changelog)
          * Notificar suporte
    """
    nome_executavel = output_folder() + "\\Ello.exe"

    build_project()
    signtool.sign(nome_executavel)
    atualiza_changelog()
    deployer.deploy(nome_executavel)
    instalador.build_and_deploy()
    wiki.atualiza_wiki()

    if len(sys.argv)==2:
        notificador.notifica()

def build_and_deploy_pre_release():
    nome_executavel = output_folder() + "\\Ello.exe"
    build_project()
    signtool.sign(nome_executavel)
    deployer.deploy(nome_executavel, pasta_destino='/home/ftp/Downloads/beta')

def build_and_deploy_silently():
    """ Build e deploy silencioso
    """
    ello.build()
    deployer.deploy()

def deploy_test_version():
    gera_resources()
    delphi.build_project("Ello.dpr", True)
    print "Enviando arquivo para a pasta de testes..."
    hora = datetime.datetime.now().strftime('%H%M%S')
    shutil.copyfile('C:/Ello/Windows/Ello.exe', '\\\\10.1.1.100\\transferencia\\Wayron\\testar\\Ello-TESTDRIVE-{}.exe'.format(hora))

def build_project():
    remove_dcus()
    gera_arquivo_resource()
    delphi.build_project("Ello.dpr", debug=False)
    
def atualiza_changelog():
    changelog.update()
    versao = '.'.join(versao_no_changelog())
    repositorio.cria_tag_versao(versao)
    repositorio.commita_changelog(versao)

def output_folder():
    config = ConfigParser()
    config.read("Ello.dof")
    return config.get("Directories", "OutputDir")

def remove_dcus():
    map(os.remove, glob.glob("dcu/*.dcu"))

def versao_no_changelog():
    with open('CHANGELOG.txt', 'r') as f:
        versao = f.readline()
    r = re.search(u'são (\d+\.\d+.\d+(\.\d+)*)', versao)
    versao = r.group(1).split('.')
    if len(versao)==3:
        versao.append('0')
    return versao

def clean_working_dir():
    os.system('del /s *.ddp')
    os.system('del /s *.dsk')
    os.system('del /s *.dcu')
    os.system('del /s *.~*')

def gera_resources():
    gera_arquivo_resource()
    delphi.resource_compile("Ello.rc", "Ello.res")

def gera_arquivo_resource():
    major, minor, build, release = versao_no_changelog()
    print u"Gerando arquivo resources da versão %s" % ".".join(versao_no_changelog())

    grava_arquivo_resource(major, minor, build, release, BUILD_INFO)
    delphi.resource_compile("Ello.rc", "Ello.res")

    # Remove informacoes de build para deixar o arquivo rc sem as informações de build
    grava_arquivo_resource(major, minor, build, release, '')

def grava_arquivo_resource(major, minor, build, release, build_info):
    f = open('Ello.rc', 'w')
    file_content = RC_FILE.format(major=major, 
                                  minor=minor, 
                                  build=build, 
                                  release=release,
                                  build_info=build_info)
    file_content = file_content.encode('latin1')
    f.write(file_content)
    f.close()

if __name__=="__main__":
    build()

