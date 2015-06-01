#coding: utf8
import os
import re
import glob
import delphi
from utils import memoize
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
            VALUE "InternalName", ""
            VALUE "LegalCopyright", "Ello Tecnologia Ltda\\0"
            VALUE "LegalTrademarks", ""
            VALUE "OriginalFilename", ""
            VALUE "ProductName", "Sistema Ello\\0"
            VALUE "ProductVersion", "{major}.{minor}\\0"
            VALUE "Comments", ""
        END
    END

    BLOCK "VarFileInfo"
    BEGIN
        VALUE "Translation", 0x0416 0x04E4
    END
END
"""

@memoize
def versao_no_changelog():
    with open('CHANGELOG.txt', 'r') as f:
        versao = f.readline()
    r = re.search(u'são (\d+\.\d+.\d+(\.\d+)*)', versao)
    versao = r.group(1).split('.')
    if len(versao)==3:
        versao.append('0')
    return versao

def output_folder():
    config = ConfigParser()
    config.read("Ello.dof")
    return config.get("Directories", "OutputDir")

def remove_dcus():
    print "Removendo arquivos dcu..."
    map(os.remove, glob.glob("dcu/*.dcu"))

def gera_arquivo_resource():
    major, minor, build, release = versao_no_changelog()
    print u"Gerando arquivo resources da versão %s" % ".".join(versao_no_changelog())

    f = open('Ello.rc', 'w')
    file_content = RC_FILE.format(major=major, 
                                  minor=minor, 
                                  build=build, 
                                  release=release)
    file_content = file_content.encode('latin1')
    f.write(file_content)
    f.close()

    delphi.resource_compile("Ello.rc", "Ello.res")

def build():
    remove_dcus()
    gera_arquivo_resource()
    delphi.build_project("Ello.dpr", debug=False)
    print "Arquivo gerado em", output_folder()
    
if __name__=="__main__":
    build()

