#coding: utf8
import sys
import os
import fnmatch
import argparse
import re
import fdb

import pywintypes
from win32com.client import Dispatch

def log(message):
    #print message.encode('latin1')
    print message

def relatorios():
    """ Generator que retorna todos os relatórios contidos na pasta relatórios do Ello
    """
    for root, dirnames, filenames in os.walk('C:\\ello\\relatorios'):
        for filename in fnmatch.filter(filenames, '*.rpt'):
            filename = os.path.join(root, filename).decode('latin-1')
            if u'Relatórios Bugados' in filename:
                continue
            yield filename

def open_crystal_report(report_filename):
    """ Cria uma instância do relatório crystal
    """
    app = Dispatch('CrystalRunTime.Application')
    rep = app.OpenReport(report_filename)
    rep.enableParameterPrompting = False
    return rep

def search(report, filename, search_term):
    """ Faz a busca de um termo na Query String do relatório
    """
    try:
        result = re.search(search_term, report.sqlquerystring, re.IGNORECASE)
    except pywintypes.com_error as e:
        log(u"Erro => ({0}) {1}".format(filename, e[2]))
        result = False
    return result

def validate_report_query_function():
    conn = fdb.connect('/ello/dados/testes/TESTES-1.2.53.ELLO')
    def validate_query_function(report_filename, report):
        cursor = conn.cursor()
        if 'Lista de Clientes.rpt' in report_filename:
            import pdb; pdb.set_trace()
        for query in extract_selects(report.sqlquerystring):
            query = define_filter_values(query)
            try:
                cursor.execute(query)
            except fdb.DatabaseError as e:
                log(u'Erro no relatório "{0}"'.format(report_filename))
                log(u"{0}".format(e[0]))
                log(u"\n{0}\n".format(query))
                log(u"---------")
    return validate_query_function

def extract_selects(sqlquery):
    queries = sqlquery.lower().split('select')
    for query in queries:
        if not query:
            continue
        query = query.replace('"', '')
        yield 'select ' + query

def define_filter_values(sqlquery):
    query = sqlquery
    query = re.sub('\{\?filtro\}',          '',              query,  flags=re.I)
    query = re.sub('\{\?filter\}',          '',              query,  flags=re.I)
    query = re.sub('\{\?where\}',           '',              query,  flags=re.I)
    query = re.sub('\{\?empresa\}',         '1',             query,  flags=re.I)
    query = re.sub('\{\?pEmpresa\}',        '1',             query,  flags=re.I)
    query = re.sub('\{\?IdEmpresa\}',       '1',             query,  flags=re.I)
    query = re.sub('\{\?IdPedido\}',        '1',             query,  flags=re.I)
    query = re.sub('\{\?IdNota\}',          '1',             query,  flags=re.I)
    query = re.sub('\{\?IdRegistro\}',      '1',             query,  flags=re.I)
    query = re.sub('\{\?IdInventario\}',    '1',             query,  flags=re.I)
    query = re.sub('\{\?IdDocumento\}',     '1',             query,  flags=re.I)
    query = re.sub('\{\?IdBaixa\}',         '1',             query,  flags=re.I)
    query = re.sub('\{\?idcliente\}',       '1',             query,  flags=re.I)
    query = re.sub('\{\?fornecedor\}',      '1',             query,  flags=re.I)
    query = re.sub('\{\?IdPeriodo\}',       '1',             query,  flags=re.I)
    query = re.sub('\{\?pIdCentroCusto\}',  '1',             query,  flags=re.I)
    query = re.sub('\{\?pIdPlanoConta\}',   '1',             query,  flags=re.I)
    query = re.sub('\{\?IDPLCONTA\}',       '1',             query,  flags=re.I)
    query = re.sub('\{\?pDataInicial\}',    "'01.01.2001'",  query,  flags=re.I)
    query = re.sub('\{\?pDataFinal\}',      "'01.01.2001'",  query,  flags=re.I)
    query = re.sub('\{\?FiltroAux\}',       '',              query,  flags=re.I)
    query = re.sub('\{\?DataInicial\}',     "'01.01.2001'",  query,  flags=re.I)
    query = re.sub('\{\?DataFinal\}',       "'01.01.2001'",  query,  flags=re.I)
    query = re.sub('\{\?AnoMes\}',          "'201701'",      query,  flags=re.I)
    query = re.sub('\{\?IdAlmox\}',         "1",             query,  flags=re.I)
    query = re.sub('\{\?DataIni\}',         "'01.01.2001'",  query,  flags=re.I)
    query = re.sub('\{\?DataFim\}',         "'01.01.2001'",  query,  flags=re.I)
    query = re.sub('\{\?ADtaIn\}',          "'01.01.2001'",  query,  flags=re.I)
    query = re.sub('\{\?BDtaFim\}',         "'01.01.2001'",  query,  flags=re.I)
    query = re.sub('\{\?FilterBaixas1\}',   "",              query,  flags=re.I)
    query = re.sub('\{\?FilterBaixas2\}',   "",              query,  flags=re.I)
    query = re.sub('\{\?FilterVendas1\}',   "",              query,  flags=re.I)
    query = re.sub('\{\?Ano\}',             "'2017'",        query,  flags=re.I)
    query = re.sub('\{\?Tipo\}',            "1",             query,  flags=re.I)
    query = re.sub('\{\?dta\}',             "'01.01.2001'",  query,  flags=re.I)
    query = re.sub('\{\?dtb\}',             "'01.01.2001'",  query,  flags=re.I)
    return query

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', dest='search_term')
    parser.add_argument('-v', '--validate-query', action='store_true', help=u'Testa a query do relatório')
    return parser.parse_args()

if __name__=="__main__":
    args = parse_args()
    validate_report_query = validate_report_query_function()

    for filename in relatorios():
        report = open_crystal_report(filename)
        if args.search_term:
            if search(report, filename, args.search_term):
                log(filename)
        elif args.validate_query:
            validate_report_query(filename, report)
        else:
            sys.exit(0)

