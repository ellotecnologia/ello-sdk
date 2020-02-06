#coding: utf8
""" Tenta corrigir problemas em um projeto Delphi de acordo com o tipo de Problema 
    relatado pelo compilador.
"""
import sys
import subprocess
import fileinput
import re

from delphi.errors import (
    CompilationError,
    UndeclaredIdentifierError,
    IdentifierRedeclaredError,
    FileNotFoundError
)

def try_to_compile_project(project_name):
    p = subprocess.Popen(['dcc32', '-q', project_name], stdout=subprocess.PIPE)
    lines = p.communicate()[0].split('\n')
    for line in lines:
        if ('Error:' in line) or ('Fatal:' in line):
            error = extract_error(project_name, line)
            print(error)
            return error
    return None

def extract_error(project_name, line):
    if 'Undeclared identifier' in line:
        error = UndeclaredIdentifierError(project_name, line)
    elif 'File not found' in line:
        error = FileNotFoundError(project_name, line)
    elif 'Identifier redeclared' in line:
        error = IdentifierRedeclaredError(project_name, line)
    else:
        error = CompilationError(project_name, line)
    return error

def main(project_name):
    ultima_unit_alterada = ''
    while True:
        error = try_to_compile_project(project_name)
        if not error:
            break
        #if error.unit_name == ultima_unit_alterada:
        #    print u"Circular error".format(error.unit_name)
        #    sys.exit(1)
        ultima_unit_alterada = error.unit_name
        error.apply_fix()

if __name__=="__main__":
    main(sys.argv[1])

# Ideia
# ell mass-fix 
#   --add-implementation-unint=unit_name
#   --add-interface-unit=unit_name
#   --remove-implementation-unit=u
#   --rename-unit=unit_name