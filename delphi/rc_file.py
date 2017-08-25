#coding: utf8
import os
import logging
import subprocess

logger = logging.getLogger()

DELPHI_PATH = os.getenv('DELPHI_BIN')
BUILD_INFO = """
#define OFFICIAL_BUILD_INFO 3556

STRINGTABLE
BEGIN
  OFFICIAL_BUILD_INFO, "Official Build"
END
"""

def update_resource_file(project_name, major, minor, build, release=0):
    logger.info(u"Gerando arquivo resources da versão {0}.{1}.{2}.{3}".format(major, minor, build, release))
    create_resource_file(project_name, major, minor, build, release, BUILD_INFO)
    compile_resource_file('{0}.rc'.format(project_name))
    # Remove informacoes de build para deixar o arquivo rc sem as informações de build
    create_resource_file(project_name, major, minor, build, release, '')

def create_resource_file(project_name, major, minor, build, release, build_info):
    template = get_template_file_contents()
    with open('{0}.rc'.format(project_name), 'w') as f:
        file_content = template.format(
            project_name=project_name,
            major=major, 
            minor=minor, 
            build=build, 
            release=release,
            build_info=build_info)
        f.write(file_content.encode('latin1'))

def get_template_file_contents():
    root_path = os.path.dirname(__file__) 
    with open(root_path + '\\resource_file.template', 'r') as template_file:
        template = template_file.read().decode('utf8')
    return template

def compile_resource_file(resource_filename):
    logger.info(u"Compilando arquivo de resources {0}".format(resource_filename))
    output_filename = resource_filename.replace('.rc', '.res')
    params = "{0}\\brcc32 {1} -fo{2}".format(DELPHI_PATH, resource_filename, output_filename)
    with open(os.devnull, 'wb') as FNULL:
        subprocess.call(params.split(), stdout=FNULL)

