# encoding: utf8
""" Reads units from a Delphi project and update 
    a Test Project with correct unit paths.
"""
import sys
import string
import os.path
import fileinput


def find_uses_section(project_file):
    """ Reads a file until it finds it's 'Uses' section
    """
    while True:
        line = project_file.readline()
        if not line:
            break
        if line.startswith('uses'):
            return
    raise Exception('Uses section not found')


def load_unit_names(project_file):
    """ Returns a list of the unit lines inside a project file
    """
    units = []
    for line in project_file:
        line = line.strip()
        is_last_unit = line.endswith(';')
        line = line.replace(';', ',')
        units.append(line)
        if is_last_unit:
            break
    return units


def load_project_units(project_filename):
    with open(project_filename, 'r') as project_file:
        find_uses_section(project_file)
        unit_names = load_unit_names(project_file)
    return unit_names


def adjust_unit_path(unit_line, path):
    return unit_line.replace("in '", "in '"+path)


def load_overrided_units():
    if not os.path.isfile('.unitoverrides'):
        return None
    with open('.unitoverrides', 'r') as f:
        units = map(string.strip, f.readlines())
    return units


def unit_overrided(unit_line, overrided_units):
    if not overrided_units:
        return False
    for unit in overrided_units:
        if unit in unit_line:
            return True
    return False


def update_test_project(test_project_file, tested_project_file):
    new_path = os.path.dirname(tested_project_file) + "\\"
    units = load_project_units(tested_project_file)
    units = map(lambda l: adjust_unit_path(l, new_path), units)
    overrided_units = load_overrided_units()
    inside_markers = False
    for line in fileinput.input(test_project_file, inplace=True):
        inside_markers = ('<TestedProjectUnits>' in line) or inside_markers

        if inside_markers:
            if '</TestedProjectUnits>' in line:
                print("  // <TestedProjectUnits>")
                inside_markers = False
                for unit in units:
                    if not unit_overrided(unit, overrided_units):
                        print '  ' + unit
                print("  // </TestedProjectUnits>")
        else:
            print line,


if __name__ == "__main__":
    test_project_file = sys.argv[1]
    tested_project_file = sys.argv[2]
    update_test_project(test_project_file, tested_project_file)