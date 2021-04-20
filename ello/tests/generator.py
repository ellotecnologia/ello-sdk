import sys
import os
import fileinput
import re

from pathlib import Path

test_template = """\
unit U<sut>Tests;

interface

uses ExlTests, U<sut>;

type
  T<sut>Tests = class(TTestCase)
  private
    <sut>: T<sut>;
  protected
    procedure Setup; override;
    procedure Teardown; override;
  published
    procedure Teste;
  end;

implementation

uses UFirebird;

{ T<sut>Tests }

procedure T<sut>Tests.Setup;
begin
   inherited;
   StartTransaction;
end;

procedure T<sut>Tests.Teardown;
begin
   <sut>.Free;
   RollbackTransaction;
   inherited;
end;

procedure T<sut>Tests.Teste;
begin

end;

initialization
   RegisterTest('<sut>', T<sut>Tests.Suite);

end.
"""

def generate_test_case(args):
    """ Gera um arquivo de TestCase DUnit de acordo com o modelo acima.
    """
    folder, unit_name = os.path.split(args.sut)
    sut = os.path.splitext(unit_name)[0][1:]

    test_project = args.dpr or 'tests/Integration/IntegrationTests.dpr'
     
    tests_path = os.path.dirname(test_project)
    test_unit = tests_path + folder + '\\U' + sut + 'Tests.pas'
    
    if os.path.exists(test_unit):
        print('Test suite já existe:')
        print('  ' + test_unit)
        return

    # Gravar a unit
    Path(tests_path + folder).mkdir(parents=True, exist_ok=True)
    with open(test_unit, 'wb') as f:
        f.write(test_template.replace('<sut>', sut).encode('latin1'))

    # Atualizar .dpr
    unit_line_re = re.compile("\s+\w+\s+in\s+'.+';")
    for line in fileinput.input(files=(test_project,), inplace=True):
        if unit_line_re.match(line):
            sys.stdout.write(line.replace(';', ','))
            sys.stdout.write(f"  U{sut}Tests in '{folder}\\U{sut}Tests.pas';\n")
        else:
            sys.stdout.write(line)
