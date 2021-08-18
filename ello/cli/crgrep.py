"""
Busca relatórios .rpt (crystal reports) que contenham o termo informado
"""
import sys
import re
import glob
import pywintypes
from win32com.client import Dispatch

SUBREPORT_KIND = 5


def search_in_report(search_term, report_file):
    app = Dispatch('CrystalRunTime.Application')
    report = app.OpenReport(report_file)
    
    if _search_in_report(search_term, report):
        print(f'Found in "{report_file}"')

    for section in report.Sections:
        for report_object in section.ReportObjects:
            if report_object.Kind == SUBREPORT_KIND:
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


def search_in_all_reports(search_term):
    for filename in glob.glob(r"C:\ello\relatorios\**\*.rpt", recursive=True):
        search_in_report(search_term, filename)


def main():
    if len(sys.argv) == 1:
        print('CRGrep busca o termo informado em Relatórios .rpt (Crystal Reports)')
        print('')
        print('Uso: crgrep [arquivo_relatorio] <termo_pesquisado>')
        sys.exit(1)

    if len(sys.argv) == 2:
        search_term = sys.argv[1]
        search_in_all_reports(search_term)
    elif len(sys.argv) == 3:
        rpt_file = sys.argv[1]
        search_term = sys.argv[2]
        search_in_report(search_term, rpt_file)


if __name__ == "__main__":
    main()