import sys
import os
import fnmatch
import argparse
import re
import fdb
import glob

import pywintypes
from win32com.client import Dispatch

# CRAreaKind
crReportHeader = 1
crPageHeader   = 2
crGroupHeader  = 3
crDetail       = 4
crGroupFooter  = 5
crPageFooter   = 7
crReportFooter = 8

# CRObjectKind
crFieldObject     = 1
crTextObject      = 2
crLineObject      = 3
crBoxObject       = 4
crSubreportObject = 5
crOleObject       = 6
crGraphObject     = 7
crCrossTabObject  = 8
crBlobFieldObject = 9
crMapObject       = 10
crOlapGridObject  = 11

CRPaperOrientation = {
    0: 'crDefaultPaperOrientation',
    2: 'crLandscape',
    1: 'crPortrait'
}

CRPaperSize = {
    9: 'crPaperA4'
}

CRAreaKind = {
    crReportHeader : 'crReportHeader',
    crPageHeader   : 'crPageHeader',
    crGroupHeader  : 'crGroupHeader',
    crDetail       : 'crDetail',
    crGroupFooter  : 'crGroupFooter',
    crPageFooter   : 'crPageFooter',
    crReportFooter : 'crReportFooter'
}

CRObjectKind = {
    crFieldObject     : 'crFieldObject',
    crTextObject      : 'crTextObject',
    crLineObject      : 'crLineObject',
    crBoxObject       : 'crBoxObject',
    crSubreportObject : 'crSubreportObject',
    crOleObject       : 'crOleObject',
    crGraphObject     : 'crGraphObject',
    crCrossTabObject  : 'crCrossTabObject',
    crBlobFieldObject : 'crBlobFieldObject',
    crMapObject       : 'crMapObject',
    crOlapGridObject  : 'crOlapGridObject'
}

def search_in_all_reports(search_term):
    for filename in glob.glob('C:\\Ello\\relatorios\\**\\*.rpt', recursive=True):
        search_in_report(search_term, filename)


def search_in_report(search_term, report_file):
    app = Dispatch('CrystalRunTime.Application')
    report = app.OpenReport(report_file)
    
    if _search_in_report(search_term, report):
        print(f'Found in "{report_file}"')

    found, formula_field = search_formula_fields(search_term, report)
    if found:
        print(f'Found in "{report_file}", Formula Field "{formula_field}"')
        return
    
    # Search term inside sub-reports
    for section in report.Sections:
        for report_object in section.ReportObjects:
            if report_object.Kind == crSubreportObject:
                subreport = report_object.OpenSubreport()
                if _search_in_report(search_term, subreport):
                    print(f'Found in "{report_file}" section ' + report_object.Name)


def _search_in_report(search_term, report):
    report.enableParameterPrompting = False
    
    try:
        if search_term.lower() in report.sqlquerystring.lower():
            return True
    except pywintypes.com_error as e:
        #print(f'Error in "{report_file}":\n\t{e.args}')
        print(f'Error:\n\t{e.args}')

    return False


def list_query_string(filename):
    report = open_crystal_report(filename)
    print(report.sqlquerystring)
    for section in report.Sections:
        for report_object in section.ReportObjects:
            if report_object.Kind == crSubreportObject:
                subreport = report_object.OpenSubreport()
                subreport.enableParameterPrompting = False
                print(subreport.sqlquerystring)


def log(message):
    print(message)


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
        result = re.search(search_term, report.sqlquerystring, flags=re.I)
    except pywintypes.com_error as e:
        log(u"Erro => ({0}) {1}".format(filename, e))
        result = False
    return result


def search_formula_fields(search_term, report):
    """Procura pelo termo 'search_term' em todo os Formula Fields do relatório"""
    for ff in report.FormulaFields:
        #print(f'Formula Field: {ff.Name } = {ff.Text}')
        #print(f'Searching in Formula Field: {ff.Name } = {ff.Text}')
        if re.search(search_term, ff.Text, flags=re.I):
            return (True, ff.Name)
    return (False, 'not found')


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
    parser.add_argument('-v', '--validate-query', action='store_true', help='Testa a query do relatório')
    parser.add_argument('-l', '--list-query-string', nargs="?", help='Lista a Query String do Relatório/SubRelatórios')
    return parser.parse_args()


def main():
    args = parse_args()
    
    if args.list_query_string:
        list_query_string(args.list_query_string)
        sys.exit(0)
    
    for filename in glob.glob(r"C:\ello\relatorios\**\*.rpt", recursive=True):
        report = open_crystal_report(filename)
        if args.search_term:
            if search(report, filename, args.search_term):
                print(filename)
        elif args.validate_query:
            validate_report_query = validate_report_query_function()
            validate_report_query(filename, report)
        else:
            sys.exit(0)


def show_report_structure(report_name):
    """Exibe a estrutura de um relatório Crystal de forma textual"""
    report = open_crystal_report(report_name)
    print('PaperOrientation:', CRPaperOrientation[report.PaperOrientation])
    print('PaperSize:', CRPaperSize[report.PaperSize])
    
    for area in report.Areas:
        if (area.Kind == crGroupHeader) or (area.Kind == crGroupFooter):
            print(f'{CRAreaKind[area.Kind]}: {area.Name} GroupConditionField: {area.GroupConditionField.Name}')
        else:
            print(f'{CRAreaKind[area.Kind]}: {area.Name}')
        
        for section in area.Sections:
            print(f'\tSection {section.Number}: {section.Name} Height: {section.Height} Width: {section.Width} Suppress: {section.Suppress}')
            for obj in section.ReportObjects:
                if obj.Kind == crTextObject:
                    print(f'\t\t{CRObjectKind[obj.Kind]}: {obj.Name} Text: {obj.Text} Top: {obj.Top} Left: {obj.Left}')
                    for fe in obj.FieldElements:
                        print(f'\t\t\t{fe.FieldDefinition.Name}')
                elif obj.Kind == crFieldObject:
                    print(f'\t\t{CRObjectKind[obj.Kind]}: {obj.Name} FieldName: {obj.Field.Name} Top: {obj.Top} Left: {obj.Left}')
                else:
                    print(f'\t\t{CRObjectKind[obj.Kind]}: {obj.Name} Top: {obj.Top} Left: {obj.Left}')
    print(report.sqlquerystring)

                    
if __name__=="__main__":
    #main()
    show_report_structure(r'C:\ello\relatorios\OrdemFechamento.rpt')
