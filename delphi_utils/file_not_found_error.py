import fnmatch
import os
import re
import fileinput

from delphi_utils.compilation_error import CompilationError

class UnitNotFound(Exception):
    pass

class FileNotFoundError(CompilationError):
    """
    >>> error = FileNotFoundError(r"ModuleName\UnitName.pas(2037) Fatal: File not found: 'MyUnit.dcu'")
    >>> error.unit_name
    'ModuleName\\\\UnitName.pas'
    >>> error.missing_file
    'MyUnit.dcu'
    """

    def __init__(self, project_name, line):
        CompilationError.__init__(self, project_name, line)
        self.missing_file = self.extract_missing_file(line)

    def extract_missing_file(self, line):
        missing_unit = line.split('File not found:')[1]
        missing_unit = missing_unit.replace("'", '')
        return missing_unit.strip()

    def apply_fix(self):
        if 'dpk' in self.project_name:
            print("Fixing package {0}".format(self.project_name))
            self.do_package_fix()
        else:
            self.do_project_fix()
            print("Fixing project {0}".format(self.project_name))

    def do_package_fix(self):
        unit_name = self.missing_file.replace('.dcu', '')
        missing_unit_paths = self.search_missing_unit(unit_name + '.pas', '..')
        if not missing_unit_paths:
            raise UnitNotFound(self.missing_file)
        RE = re.compile(r"\w+ in '.+';")
        for line in fileinput.input(self.project_name, inplace=True):
            match = RE.search(line)
            if match:
                line = line.replace(';', ',')
                print line,
                print "  {0} in '{1}';".format(unit_name, missing_unit_paths[0])
            else:
                print line,

    def do_project_fix(self):
        pass

    def search_missing_unit(self, unit_name, search_path):
        matches = []
        for root, dirnames, filenames in os.walk(search_path):
            for filename in fnmatch.filter(filenames, unit_name):
                matches.append(os.path.join(root, filename))
        return matches

    def __repr__(self):
        return "FileNotFoundError in unit {0} ({1})".format(self.unit_name, self.missing_file)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

