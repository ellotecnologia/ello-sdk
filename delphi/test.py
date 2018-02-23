import logging
logging.basicConfig(level=logging.INFO)

from delphi import Project, Compiler
from delphi.compiler import DEBUG_MODE, RELEASE_MODE

project = Project('Ello')
project.version = '1.2.56.1234'

project.add_resource('resources\\ello.rc')
project.add_resource('resources\\extra_resources.rc')

project.build_mode = DEBUG_MODE
project.conditionals = 'RETAGUARDA'

compiler = Compiler()
compiler.build(project)

