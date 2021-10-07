"""
Busca relatórios .rpt (crystal reports) que contenham o termo informado
"""
import sys
import re

from . import crystal


def main():
    if len(sys.argv) == 1:
        print('CRGrep busca o termo informado em Relatórios .rpt (Crystal Reports)')
        print('')
        print('Uso: crgrep [arquivo_relatorio] <termo_pesquisado>')
        sys.exit(1)

    if len(sys.argv) == 2:
        search_term = sys.argv[1]
        crystal.search_in_all_reports(search_term)
    elif len(sys.argv) == 3:
        rpt_file = sys.argv[1]
        search_term = sys.argv[2]
        crystal.search_in_report(search_term, rpt_file)


if __name__ == "__main__":
    main()