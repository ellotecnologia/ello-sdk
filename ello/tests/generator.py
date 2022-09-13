import sys
import os
import fileinput
import re

from pathlib import Path

TEST_TEMPLATE = """\
unit U<tested_unit>Tests;

interface

uses ExlTests, U<tested_unit>;

type
  T<tested_unit>Tests = class(TTestCase)
  private
    <tested_unit>: T<tested_unit>;
  protected
    procedure Setup; override;
    procedure Teardown; override;
  published
    procedure Teste;
  end;

implementation

uses ExlFirebird;

{ T<tested_unit>Tests }

procedure T<tested_unit>Tests.Setup;
begin
   inherited;
   StartTransaction;
end;

procedure T<tested_unit>Tests.Teardown;
begin
   <tested_unit>.Free;
   RollbackTransaction;
   inherited;
end;

procedure T<tested_unit>Tests.Teste;
begin
   <tested_unit> := T<tested_unit>.Create;
end;

initialization
   RegisterTest('<tested_unit>', T<tested_unit>Tests.Suite);

end.
"""

GUI_TEST_TEMPLATE = """\
unit <tested_unit>_Tests;

interface

uses GUITesting, ExlTests, <tested_unit>;

type
  T<tested_unit>_Tests = class(TGUITestCase)
  private
    Form: TF<tested_unit>;
  protected
    procedure Teardown; override;
  published
    procedure Teste;
  end;

implementation

uses ExlFirebird;

{ T<tested_unit>_Tests }

procedure T<tested_unit>_Tests.Teardown;
begin
   Form.Free;
   inherited;
end;

procedure T<tested_unit>_Tests.Teste;
begin
   Form := TF<tested_unit>.Create(nil);
end;

initialization
   RegisterTest('<tested_unit>', T<tested_unit>_Tests.Suite);

end.
"""

def generate_test_case(args):
    """ Gera um arquivo de TestCase DUnit de acordo com um dos modelos acima.
    """
    folder, unit_name = os.path.split(args.unit)
    sut = os.path.splitext(unit_name)[0]

    if '\\UI\\' in args.unit:
        test_project = 'tests/Functional/FunctionalTests.dpr'
        test_unit_name = sut + '_Tests'
        test_template = GUI_TEST_TEMPLATE
        folder = folder.replace('\\UI', '')
    else:
        test_project = args.dpr or 'tests/Integration/IntegrationTests.dpr'
        test_unit_name = 'U' + sut[1:] + 'Tests'
        sut = sut[1:]
        test_template = TEST_TEMPLATE
     
    tests_path = os.path.dirname(test_project)
    test_unit = os.path.join(tests_path, folder) + '\\' + test_unit_name + '.pas'
    
    if os.path.exists(test_unit):
        print('Test suite já existe:')
        print('  ' + test_unit)
        return

    # Gravar a unit
    (Path(tests_path) / Path(folder)).mkdir(parents=True, exist_ok=True)
    with open(test_unit, 'wb') as f:
        f.write(test_template.replace('<tested_unit>', sut).encode('latin1'))

    # Adiciona unit ao projeto (.dpr) de teste
    last_unit_line_re = re.compile("\s+\w+\s+in\s+'.+';")
    for line in fileinput.input(files=(test_project,), inplace=True):
        if last_unit_line_re.match(line):
            sys.stdout.write(line.replace(';', ','))
            sys.stdout.write(f"  {test_unit_name} in '{folder}\\{test_unit_name}.pas';\n")
        else:
            sys.stdout.write(line)
