import os
import subprocess

def build_tests():
    FNULL = open(os.devnull, 'wb')

    os.chdir('tests')
    print 'Compiling tests...'

    dcc32 = subprocess.Popen('dcc32 -DCONSOLE_TEST unit_tests'.split(), stdout=FNULL)
    exit_code = dcc32.wait()

    if exit_code>0:
        print 'Compilation error!'
        sys.exit(1)

    subprocess.call(['unit_tests.exe'])


