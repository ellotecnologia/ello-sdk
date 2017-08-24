class CompilationError:
    """
    >>> error = CompilationError(r"C:\ProjectFolder\ProblematicUnit.pas(6) Fatal: File not found: 'MyUnit.dcu'")
    >>> error.unit_name
    'C:\\\\ProjectFolder\\\\ProblematicUnit.pas'
    """

    def __init__(self, project_name, line):
        self.project_name = project_name
        self.unit_name = self.extract_unit_name(line)
        self.message = line

    def extract_unit_name(self, line):
        pos = line.index('(')
        return line[:pos].strip()

    def apply_fix(self):
        pass

    def __repr__(self):
        return "CompilationError in unit {0}".format(self.unit_name)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
