import fileinput
import string
import textwrap
import re


def units_restantes(output_units, unit_names):
    output = []
    for unit in unit_names:
        if unit not in output_units:
            output.append(unit)
    return output


def basic_delphi_units(unit_name):
    unit_list = ['windows', 'classes', 'sysutils', 'strutils', 'variants', 
                 'contnrs', 'fmtbcd', 'math', 'inifiles', 'wininet', 'dateutils',
                 'typinfo', 'comobj', 'clipbrd', 'system.ioutils', 'filectrl', 'printers',
                 'winsock', 'types', 'syncobjs']
    return unit_name.lower() in unit_list


def main_delphi_units(unit_name):
    unit_list = ['forms', 'messages', 'activex', 'mshtml', 'idcodermime', 'maskutils', 
                 'shellapi', 'xpman', 'teengine', 'series', 'chart', 'teeprocs', 'extdlgs']
    return unit_name.lower() in unit_list


def gui_delphi_units(unit_name):
    unit_list = ['buttons', 'controls', 'comctrls', 'toolwin', 'dialogs', 'extctrls', 
                 'graphics', 'menus', 'stdctrls', 'grids', 'dbgrids', 
                 'actnlist', 'imglist', 'jpeg']
    return unit_name.lower() in unit_list


def database_delphi_units(unit_name):
    unit_list = ['db', 'dbclient', 'dbctrls', 'provider', 'sqlexpr', 'ibevents', 
                 'ibdatabase', 'dbxpress', 'ibcustomdataset', 'ibquery']
    return unit_name.lower() in unit_list


def dunit_units(unit_name):
    return unit_name.startswith('Test')


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


def png_units(unit_name):
    unit_name = unit_name.lower()
    return unit_name.startswith('png')


def synapse_units(unit_name):
    unit_list = [
        'asn1util', 'blcksock', 'clamsend', 'dnssend', 'ftpsend', 'ftptsend',
        'httpsend', 'imapsend', 'laz_synapse', 'ldapsend', 'mimeinln', 'mimemess',
        'mimepart', 'nntpsend', 'pingsend', 'pop3send', 'slogsend', 'smtpsend',
        'snmpsend', 'sntpsend', 'ssl_cryptlib', 'ssl_libssh2', 'ssl_openssl',
        'ssl_openssl_lib', 'ssl_sbb', 'ssl_streamsec', 'synachar', 'synacode',
        'synacrypt', 'synadbg', 'synafpc', 'synaicnv', 'synaip', 'synamisc', 'synaser',
        'synautil', 'synsock', 'tlntsend', 'tzutil'
    ]
    return unit_name.lower() in unit_list


def acbr_units(unit_name):
    unit_name = unit_name.lower()
    return (unit_name.startswith('acbr')) or \
           (unit_name.startswith('pcn')) or \
           (unit_name.startswith('pnfs')) or \
           (unit_name.startswith('pcte')) or \
           (unit_name.startswith('pmdfe'))


def basic_units(unit_name):
    unit_list = ['udateutils', 'urecordlock', 'logging', 'umath', 'synacode', 'httpsend']
    return unit_name.lower() in unit_list


def excellent_units(unit_name):
    unit_list = [
        'ufirebird', 'uquerybuilder', 'uactiverecord', 'speedbuttonstacked',
        'labevelell', 'stringutils'
    ]
    unit_name = unit_name.lower()
    return unit_name.startswith('ell') or \
           unit_name.startswith('exl') or \
           unit_name.startswith('excellent') or \
           (unit_name in unit_list)


def other_units(unit_name):
    unit_list = ['acao', 'numedit', 'umsgwindows', 'dnbox', 'editbox', 'ptlbox1', 
                 'synedit', 'newbox', 'vistaaltfixunit',
                 'ufirebirdeventbus']
    return unit_name.lower() in unit_list


def ello_forms(unit_name):
    m = re.match('\w{3}\d{3}\w{2,3}', unit_name)
    return bool(m)


def extract_unit_names(data):
    """ Receives a string of unit names like 'SysUtils, Classes, Contnrs'
        and returns a list: ['SysUtils', 'Classes', 'Contnrs']
    """
    lines = data.strip().splitlines()
    lines = ''.join(lines)
    lines = lines.replace(';', '')
    unit_names = lines.split(',')
    unit_names = map(str.strip, unit_names)
    return unit_names


def sort_unit_names(unit_names):
    """ Receives an unsorted list of unit names and returns a sorted list
    """
    units = []

    units.extend(list(filter(basic_delphi_units, unit_names)))
    units.extend(list(filter(main_delphi_units, unit_names)))
    units.extend(list(filter(gui_delphi_units, unit_names)))
    units.extend(list(filter(database_delphi_units, unit_names)))
    units.extend(list(filter(dunit_units, unit_names)))
    units.extend(list(filter(indy_units, unit_names)))
    units.extend(list(filter(devexpress_units, unit_names)))
    units.extend(list(filter(basic_units, unit_names)))
    units.extend(list(filter(jcl_units, unit_names)))
    units.extend(list(filter(synapse_units, unit_names)))
    units.extend(list(filter(acbr_units, unit_names)))
    units.extend(list(filter(png_units, unit_names)))
    units.extend(list(filter(excellent_units, unit_names)))
    units.extend(list(filter(other_units, unit_names)))

    forms_units = list(filter(ello_forms, unit_names)) # Extrai as units referente a forms

    remaining_units = list(filter(lambda unit: unit not in units, unit_names))
    remaining_units = list(filter(lambda unit: unit not in forms_units, remaining_units))

    units.extend(remaining_units)
    units.extend(forms_units)

    return units


def wrap_units_block(unit_names):
    output = ''
    lines = textwrap.wrap(', '.join(unit_names)+';', 120)
    for line in lines:
        output += '  ' + line + '\r\n'
    return output


def main():
    import pyperclip
    data = pyperclip.paste()
    unit_names = list(extract_unit_names(data))
    #breakpoint()
    unit_names = sort_unit_names(unit_names)
    output = wrap_units_block(unit_names)
    pyperclip.copy(output)


if __name__ == "__main__":
    main()
