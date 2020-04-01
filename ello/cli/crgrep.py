"""
Busca relatórios .rpt (crystal reports) que contenham o termo informado
"""
import sys
import re
import glob
import pywintypes
from win32com.client import Dispatch

def search_in_report(search_term, report_file):
    app = Dispatch('CrystalRunTime.Application')
    rep = app.OpenReport(report_file)
    rep.enableParameterPrompting = False
    try:
        if search_term.lower() in rep.sqlquerystring.lower():
            print(f'Found in "{report_file}"')
    except pywintypes.com_error as e:
        print(f'Error in "{report_file}":\n\t{e.args}')


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