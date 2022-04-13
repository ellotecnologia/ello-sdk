""" Sincroniza as units de um projeto de teste (.dpr) de acordo com o projeto
    testado (SUT). 
    
    Um projeto de teste delphi deve possuir em seu .dpr uma linha contendo o
    caminho do projeto testado, especificado como comentário da seguinte forma:

    ```
    program IntegrationTests;
    
    // SUT: ..\Project.dpr
    
    uses
      // <SUT-Units>
      ...
      // </SUT-Units>
    
    begin
    ...
    end.
    
    ```
"""

import sys
import string
import os.path
import fileinput

from delphi.dof import DOFFile


def get_system_under_test_path(test_project_filename):
    """ Obtém o caminho do projeto testado (SUT)
    """
    with open(test_project_filename, 'r', encoding='latin1') as source_file:
        while True:
            line = source_file.readline()
            if not line:
                break
            if line.startswith('// SUT:'):
                return line.split(':')[1].strip()
    raise Exception(f'SUT not defined in {test_project_filename}')


def goto_uses_section(source_file):
    """ Lê o arquivo até encontrar a seção 'Uses'
    """
    while True:
        line = source_file.readline()
        if not line:
            break
        if line.startswith('uses'):
            return
    raise Exception('Uses section not found')


def load_overrided_units():
    if not os.path.isfile('.unitoverrides'):
        return None
    with open('.unitoverrides', 'r') as f:
        units = map(str.strip, f.readlines())
    return units


def unit_overrided(unit_line, overrided_units):
    if not overrided_units:
        return False
    for unit in overrided_units:
        if unit in unit_line:
            return True
    return False


def sync_unit_paths(test_project_filename, sut_unit_names):
    overrided_units = load_overrided_units()
    inside_markers = False
    for line in fileinput.input(test_project_filename, inplace=True):
        inside_markers = ('<SUT-Units>' in line) or inside_markers

        if inside_markers:
            if '</SUT-Units>' in line:
                print("  // <SUT-Units>")
                inside_markers = False
                for unit in sut_unit_names:
                    if not unit_overrided(unit, overrided_units):
                        print('  ' + unit)
                print("  // </SUT-Units>")
        else:
            print(line, end='')


def load_unit_names(source_file):
    """ Retorna uma lista contendo as linhas de definição das units em 'source_file'
    """
    goto_uses_section(source_file)
    units = []
    for line in source_file:
        line = line.strip()
        is_last_unit = line.endswith(';')
        line = line.replace(';', ',')
        units.append(line)
        if is_last_unit:
            break
    return units


def fix_search_path(search_path, new_path):
    search_path = search_path.split(';')
    new_search_path = []
    for path in search_path:
        if path.startswith('..'):
            new_search_path.append(new_path + path)
        else:
            new_search_path.append(path)
    return ';'.join(new_search_path)


def update_test_project(args):
    """ Atualiza as units do Projeto de Teste (.dpr) de acordo
        com as units definidas no SUT (.dpr)
    """
    sut_project_path = get_system_under_test_path(args.test_project_path)
    sut_abspath = os.path.abspath(os.path.join(os.path.dirname(args.test_project_path), sut_project_path))
    
    # Sync unit paths
    with open(sut_abspath, 'r', encoding='latin1') as source_file:
        sut_unit_names = load_unit_names(source_file)
    new_path = os.path.dirname(sut_project_path) + "\\"
    sut_unit_names = map(lambda l: l.replace("in '", "in '" + new_path), sut_unit_names)
    sync_unit_paths(args.test_project_path, sut_unit_names)
