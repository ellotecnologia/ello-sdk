import ctypes, sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin(program):
    params = ''
    ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(program), unicode(params), None, 1)


if is_admin():
    # Code of your program here
    pass
else:
    # Re-run the program with admin rights
    run_as_admin('teste.bat')
