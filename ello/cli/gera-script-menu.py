import StringIO
import ConfigParser

import dataset

separador = "\n" + (("/* " + ("*" * 80) + " */\n") * 3) + "\n"

#Config = ConfigParser.ConfigParser()
#Config.read("c:\\ello\\windows\\ello.ini")
#caminho = Config.get('Dados', 'Database')

db = dataset.connect('firebird+fdb://sysdba:masterkey@//ello/dados/ZERADO-1.2.55.ELLO')

def extrai_modulos(output):
    output.write(separador)
    query = "UPDATE OR INSERT INTO TGERMODULO (IDMODULO, DESCRICAO, TIPOEMPRESA) VALUES ('{0}', '{1}', '{2}');\n"
    modulos = db['TGERMODULO'].find(order_by=['idmodulo'])
    for row in modulos:
        output.write(query.format(row['idmodulo'], row['descricao'], row['tipoempresa']))
    output.write('COMMIT;\n')

def extrai_programas(output):
    output.write(separador)
    query = ("UPDATE OR INSERT INTO TGERPROGRAMA (IDPROGRAMA, PROGRAMA, DESCRICAO, "
             "OBSERVACAO, TIPO, MODULO, IDPESQUISA, PESQINCREMENTAL, TAG, COMISSAO) "
             "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}' );\n")
    programas = db['TGERPROGRAMA'].find(order_by=['idprograma'])
    for row in programas:
        output.write(query.format(row['idprograma'], row['programa'], row['descricao'], row['observacao'], \
                                  row['tipo'], row['modulo'], row['idpesquisa'], row['pesqincremental'], row['tag'], row['comissao']))
    output.write('COMMIT;\n')
    
def extrai_menus(output):
    output.write(separador)
    query = ("INSERT INTO TGERMENU (IDMENU, IDMENUPARENT, DESCRICAO, TIPO, IMAGEM, IDPROGRAMA, EMPRESA, USUARIO) "
             "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}');\n")
    menus = db['TGERMENU'].find(order_by=['idmenu'])
    for row in menus:
        insert_query = query.format(row['idmenu'], row['idmenuparent'], row['descricao'], row['tipo'], \
                                    row['imagem'], row['idprograma'], row['empresa'], row['usuario'])
        insert_query = insert_query.replace("'None'", "NULL")
        output.write(insert_query)
    output.write('COMMIT;\n')
            
def extrai_relatorios(output):
    output.write(separador)
    query = ("UPDATE OR INSERT INTO TGERRELATORIOS (IDRELATORIO, TITULO, TAG, DESCRICAO, CAMINHO, PROGRAMA, USUARIO) "
             "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}');\n")
    relatorios = db['TGERRELATORIOS'].find(order_by=['idrelatorio'])
    for row in relatorios:
        output.write(query.format(row['idrelatorio'], row['titulo'], row['tag'], row['descricao'], row['caminho'], row['programa'], row['usuario']))
    output.write('COMMIT;\n')
        
def extrai_autonomias(output):
    output.write(separador)
    query = ("UPDATE OR INSERT INTO TGERAUTONOMIA (IDAUTONOMIA, "
             "IDAUTONOMIAPARENT, MODULO, DESCRICAO, "
             "MENSAGEM, PADRAO, TIPOVALOR, VISIVEL "
             "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}');\n")
    autonomias = db['TGERAUTONOMIA'].find(order_by=['idautonomia'])
    for row in autonomias:
        output.write(query.format(row['idautonomia'], row['idautonomiaparent'], row['modulo'], row['descricao'], row['mensagem'], row['padrao'], row['tipovalor'], row['visivel']))
    output.write('COMMIT;\n')

def monta_script():    
    output = StringIO.StringIO()
    extrai_modulos(output)
    extrai_programas(output)
    extrai_menus(output)
    extrai_relatorios(output)
    extrai_autonomias(output)
    result = output.getvalue()
    output.close()
    return result
    
f = open("Programas.sql", "w")
f.write(monta_script())
f.close()

