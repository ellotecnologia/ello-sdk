#coding: utf8
import sys
import os
import fnmatch
import argparse
import re
import fdb
from win32com.client import Dispatch

def log(message):
    #print message.encode('latin1')
    print message

def crystal_report(report_filename):
    """ Cria uma instância do relatório crystal
    """
    app = Dispatch('CrystalRunTime.Application')
    rep = app.OpenReport(report_filename)
    rep.enableParameterPrompting = False
    return rep

def search(report, search_term):
    """ Faz a busca de um termo na Query String do relatório
    """
    return re.search(search_term, report.sqlquerystring, re.IGNORECASE)

#rep.sqlquerystring = 'select idproduto as idcliente, descricao as nome from testproduto'
#rep.Set_SQLQueryString('select idproduto as idcliente, descricao as nome from testproduto')
#rep.ReadRecords()

#rep.viewreport()
#print rep.SQLQueryString

def test_query_function():
    conn = fdb.connect('/ello/dados/prestativa2.ello')
    def test_query(report_filename, report):
        cursor = conn.cursor()
        try:
            query = re.sub('\{\?\w+\}', '', report.sqlquerystring)
            query = re.sub('\{\?empresa\}', '1', query, re.I)
            query = re.sub('\{\?fornecedor\}', '1', query, re.I)
        except:
            log(u"Erro na abertura do relatório {0}".format(report_filename))
            return

        try:
            cursor.execute(query)
        except fdb.DatabaseError, E:
            log(u'Erro no relatorio "{0}"'.format(report_filename))
            #raise
    return test_query

def relatorios():
    """ Generator que retorna todos os relatórios contidos na pasta relatórios do Ello
    """
    for root, dirnames, filenames in os.walk('C:\\ello\\relatorios'):
        for filename in fnmatch.filter(filenames, '*.rpt'):
            yield os.path.join(root, filename)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', dest='search_term')
    parser.add_argument('-t', '--test-query', action='store_true', help='Testa a query encontrada')
    return parser.parse_args()

if __name__=="__main__":
    args = parse_args()
    test_function = test_query_function()

    for report_filename in relatorios():
        report_filename = report_filename.decode('latin-1')
        relatorio_crystal = crystal_report(report_filename)
        if args.search_term:
            if search(relatorio_crystal, args.search_term):
                log(report_filename)
                if args.test_query:
                    test_function(report_filename, relatorio_crystal)
        elif args.test_query:
            #print u'Testando relatório', report_filename
            test_function(report_filename, relatorio_crystal)
        else:
            sys.exit(0)

