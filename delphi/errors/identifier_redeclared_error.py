import re
import fileinput

from .compilation_error import CompilationError

class IdentifierRedeclaredError(CompilationError):
    """
    >>> error = IdentifierRedeclaredError("Ello", r"Estoque\UProduto.pas(6) Error: Identifier redeclared: 'UActiveRecord'")
    >>> error.unit_name
    'Estoque\\\\UProduto.pas'
    >>> error.identifier
    'UActiveRecord'
    """
    
    def __init__(self, project_name, line):
        CompilationError.__init__(self, project_name, line)
        self.identifier = self.extract_identifier_name(line)

    def extract_identifier_name(self, line):
        m = re.search("Identifier redeclared: '(\w+)'", line)
        return m.group(1)

    def apply_fix(self):
        """ Adiciona na uses alguma unit que esteja faltando
        """
        error = self
        print('Fixing Identifier Redeclared error... Unit: {0} Identifier: {1}'.format(error.unit_name, error.identifier))
        
        RE1 = re.compile(r', {0},'.format(error.identifier))
        RE2 = re.compile(r',{0}\b'.format(error.identifier))
        RE3 = re.compile(r'\b{0},'.format(error.identifier))
        
        for line in fileinput.input(error.unit_name, inplace=True):
            match1 = RE1.search(line)
            match2 = RE2.search(line)
            match3 = RE3.search(line)
            if match1 or match2 or match3:
                if match1:
                   line = re.sub(RE1.pattern, ', ', line)
                elif match2:
                   line = re.sub(RE2.pattern, ',', line)
                elif match3:
                   line = re.sub(RE3.pattern, '', line)
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