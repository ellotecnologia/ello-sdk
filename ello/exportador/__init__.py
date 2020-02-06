# encoding: utf8
from __future__ import unicode_literals, print_function

from configparser import ConfigParser
import string
import fdb

PROGRAMAS_SELECT = """\
SELECT 
  r.IDPROGRAMA, r.PROGRAMA, r.DESCRICAO, r.OBSERVACAO, r.TIPO, r.MODULO,
  r.IDPESQUISA, r.PESQINCREMENTAL, r.TAG, r.COMISSAO
FROM TGERPROGRAMA r
ORDER BY IdPrograma
"""
PROGRAMAS_INSERT = (
    "UPDATE OR INSERT INTO TGERPROGRAMA "
    "(IDPROGRAMA, PROGRAMA, DESCRICAO, OBSERVACAO, TIPO, MODULO, IDPESQUISA, PESQINCREMENTAL, TAG, COMISSAO) "
    "VALUES "
    "({IDPROGRAMA}, '{PROGRAMA}', '{DESCRICAO}', '{OBSERVACAO}', {TIPO}, {MODULO}, NULL, '{PESQINCREMENTAL}', {TAG}, '{COMISSAO}');"
)


MENUS_CABECALHO = "DELETE FROM TGERMENU;\n"
MENUS_RODAPE = "\nCOMMIT WORK;"
MENUS_SELECT = "SELECT * FROM TGerMenu ORDER BY IdMenu, IdMenuParent"
MENUS_INSERT = (
    "INSERT INTO TGERMENU "
    "(IDMENU, IDMENUPARENT, DESCRICAO, TIPO, IMAGEM, IDPROGRAMA, EMPRESA, USUARIO) "
    "VALUES "
    "({IDMENU}, {IDMENUPARENT}, '{DESCRICAO}', {TIPO}, {IMAGEM}, {IDPROGRAMA}, {EMPRESA}, 'ADMINISTRADOR');"
)


class NoneFormatter(string.Formatter):
    def __init__(self, default = ''):
        self.default = default

    def get_value(self, key, args, kwds):
        if kwds[key] is None:
            return 'NULL'
        else:
            return kwds.get(key, self.default)

fmt = NoneFormatter()

            
def exporta_menus():
    conn = obtem_conexao()
    cursor = conn.cursor()
    cursor.execute(MENUS_SELECT)
    menus = cursor.fetchallmap()
    print(MENUS_CABECALHO)
    for row in menus:
        print(fmt.format(MENUS_INSERT, **dict(row)).encode('latin1'))
    print(MENUS_RODAPE)
    cursor.close()
    conn.close()

def exporta_programas():
    conn = obtem_conexao()
    cursor = conn.cursor()
    cursor.execute(PROGRAMAS_SELECT)
    programas = cursor.fetchallmap()
    for row in programas:
        print(fmt.format(PROGRAMAS_INSERT, **dict(row)).encode('latin1'))
    print('COMMIT WORK;')
    cursor.close()
    conn.close()


def obtem_conexao():
    ini_file = '/Ello/Windows/Ello.ini'
    config = ConfigParser.RawConfigParser()
    config.read(ini_file)
    database = config.get('Dados', 'DataBase')
    return fdb.connect(database, charset='latin1')

    
if __name__ == "__main__":
    pass