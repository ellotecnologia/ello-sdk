import fileinput
import string
import textwrap
import re

import win32clipboard

def units_restantes(output_units, unit_names):
    output = []
    for unit in unit_names:
        if unit not in output_units:
            output.append(unit)
    return output

def basic_delphi_units(unit_name):
    unit_list = ['windows', 'classes', 'sysutils', 'strutils', 'variants', 
                 'contnrs', 'fmtbcd', 'math', 'inifiles', 'wininet', 'dateutils',
                 'typinfo', 'comobj']
    return unit_name.lower() in unit_list

def main_delphi_units(unit_name):
    unit_list = ['forms', 'messages', 'activex', 'mshtml', 'idcodermime', 'maskutils', 
                 'shellapi', 'xpman', 'teengine', 'series', 'chart', 'teeprocs']
    return unit_name.lower() in unit_list

def gui_delphi_units(unit_name):
    unit_list = ['buttons', 'controls', 'comctrls', 'toolwin', 'dialogs', 'extctrls', 
                 'graphics', 'menus', 'stdctrls', 'pngimage', 'grids', 'dbgrids', 
                 'pngspeedbutton', 'actnlist', 'pngbitbtn', 'imglist']
    return unit_name.lower() in unit_list

def database_delphi_units(unit_name):
    unit_list = ['db', 'dbclient', 'dbctrls', 'provider', 'sqlexpr', 'ibevents', 
                 'ibdatabase', 'dbxpress', 'ibcustomdataset', 'ibquery']
    return unit_name.lower() in unit_list

def indy_units(unit_name):
    unit_list = ['idudpbase', 'idudpserver', 'idtcpconnection', 'idtcpclient', 
                 'idantifreeze', 'idsockethandle', 'idtcpserver', 'idudpclient', 
                 'idthreadmgr', 'idantifreezebase', 'idbasecomponent', 'idcomponent', 
                 'idthreadmgrdefault', 'idiohandler', 'idiohandlersocket']
    return unit_name.lower() in unit_list

def devexpress_units(unit_name):
    unit_name = unit_name.lower()
    return (unit_name.startswith('dx')) or (unit_name.startswith('cx'))

def jcl_units(unit_name):
    unit_name = unit_name.lower()
    return unit_name.startswith('jcl')

def acbr_units(unit_name):
    unit_name = unit_name.lower()
    return (unit_name.startswith('acbr')) or (unit_name.startswith('pcn'))

def basic_units(unit_name):
    unit_list = ['stringutils', 'udateutils', 'urecordlock', 'logging', 'umath']
    return unit_name.lower() in unit_list

def excellent_units(unit_name):
    unit_list = ['ufirebird', 'uquerybuilder', 'uactiverecord', 'speedbuttonstacked']
    unit_name = unit_name.lower()
    return unit_name.startswith('ell') or unit_name.startswith('excellent') or (unit_name in unit_list)

def other_units(unit_name):
    unit_list = ['acao', 'numedit', 'umsgwindows', 'dnbox', 'editbox', 'ptlbox1', 
                 'pngimagelist', 'synedit', 'stringutils2', 'newbox']
    return unit_name.lower() in unit_list

def ello_forms(unit_name):
    m = re.match('\w{3}\d{3}\w{2,3}', unit_name)
    return bool(m)

win32clipboard.OpenClipboard()
data = win32clipboard.GetClipboardData()

lines = data.strip().splitlines()
lines = ''.join(lines)
lines = lines.replace(';', '')
unit_names = lines.split(',')
unit_names = map(string.strip, unit_names)

output_units = []

output_units.extend(filter(basic_delphi_units, unit_names))
output_units.extend(filter(main_delphi_units, unit_names))
output_units.extend(filter(gui_delphi_units, unit_names))
output_units.extend(filter(database_delphi_units, unit_names))
output_units.extend(filter(indy_units, unit_names))
output_units.extend(filter(devexpress_units, unit_names))
output_units.extend(filter(basic_units, unit_names))
output_units.extend(filter(jcl_units, unit_names))
output_units.extend(filter(acbr_units, unit_names))
output_units.extend(filter(excellent_units, unit_names))
output_units.extend(filter(other_units, unit_names))

# Extrai as units referente a forms
forms_units = filter(ello_forms, unit_names)

remaining_units = filter(lambda unit: unit not in output_units, unit_names)
remaining_units = filter(lambda unit: unit not in forms_units, remaining_units)

output_units.extend(remaining_units)
output_units.extend(forms_units)

output = ''
lines = textwrap.wrap(', '.join(output_units)+';', 120)
for line in lines:
    output += '  ' + line + '\r\n'

win32clipboard.SetClipboardText(output)
win32clipboard.CloseClipboard()

