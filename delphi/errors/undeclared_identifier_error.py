import re

from .compilation_error import CompilationError

identifier_location = {
    'iif': 'ExcellentUtils',
    'datavalida': 'UDateUtils',
    'queryopen': 'UFirebird',
    'qdatasql': 'UDateUtils',
    'datasql': 'UDateUtils',
    'diasnomes': 'UDateUtils',
}

class UndeclaredIdentifierError(CompilationError):
    """
    >>> error = UndeclaredIdentifierError(r"ModuleName\UnitName.pas(2037) Error: Undeclared identifier: 'TestIdentifier'")
    >>> error.unit_name
    'ModuleName\\\\UnitName.pas'
    >>> error.identifier
    'TestIdentifier'
    """
    
    def __init__(self, project_name, line):
        CompilationError.__init__(self, project_name, line)
        self.identifier = self.extract_identifier_name(line)

    def extract_identifier_name(self, line):
        m = re.search("Undeclared identifier: '(\w+)'", line)
        return m.group(1)

    def apply_fix(self):
        """ Adiciona na uses alguma unit que esteja faltando
        """
        error = self
        print('Fixing Undeclared Identifier error... Unit: {0} Identifier: {1}'.format(error.unit_name, error.identifier))
        uses_found = 0
        RE = re.compile(r'^\s*\b([Uu]ses)\b')
        missing_unit = identifier_location[error.identifier.lower()]
        for line in fileinput.input(error.unit_name, inplace=True):
            match = RE.search(line)
            if match:
                uses_found += 1
            if (match) and (uses_found>1):
                uses_found += 1
                line = re.sub('[Uu]ses\s*', 'uses {0}, '.format(missing_unit), line)
                print line,
            else:
                print line,

    def alternative_fix(self):
        error = self
        contador = 0
        RE = re.compile(r'\b([Uu]ses)\b')
        for line in fileinput.input(error.unit_name, inplace=True):
            match = RE.search(line)
            if match:
                contador += 1
            if (match) and (contador>1):
                contador += 1
                line = re.sub('[Uu]ses ', 'uses UConfiguracao, ', line)
                print line,
            else:
                print line,

if __name__ == "__main__":
    import doctest
    doctest.testmod()

