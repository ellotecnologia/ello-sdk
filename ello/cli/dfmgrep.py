import sys
import re
import glob
from enum import Enum
from collections import defaultdict

RE_QUERY  = re.compile('(object|inherited) (\w+): TSQLQuery')
RE_LBEDIT = re.compile('(object|inherited) (\w+): TcxLabelEdit( \[\d+\])*')

class State(Enum):
    OUTER = 1
    QUERY = 2
    STRINGLIST = 3
    LINEMERGE = 4
    PARAMS = 5
    LABELEDIT = 6

def clear_line(line):
    line = line.strip(')')
    line = line.strip('+')
    line = line.strip("'")
    line = line.strip()
    line = line.strip("'")
    return line


def parse_queries_from_dfm(filename):
    """Processa arquivos .dfm gerando um dict com o nome da query
       e suas respectivas linhas"""
    component_name = ''
    state = State.OUTER
    queries = defaultdict(list)
    with open(filename, 'r', encoding='latin1') as dfm:
        for line in dfm:
            line = line.strip()
            if not line:
                continue
            if state == State.OUTER:
                match = RE_QUERY.match(line)
                if match:
                    component_name = match.group(2)
                    state = State.QUERY
                    continue
                match = RE_LBEDIT.match(line)
                if match:
                    component_name = match.group(2)
                    state = State.LABELEDIT
            elif state == State.QUERY:
                if line == 'end':
                    state = State.OUTER
                elif line.endswith('Params = <'):
                    state = State.PARAMS
                elif 'SQL.Strings' in line:
                    state = State.STRINGLIST
            elif state == State.LABELEDIT:
                if line == 'end':
                    state = State.OUTER
                elif 'Pesquisa.Select.Strings' in line:
                    state = State.STRINGLIST
            elif state == State.PARAMS:
                if line == 'end>':
                    state = State.QUERY
            elif state == State.STRINGLIST:
                if line.endswith(')'):
                    state = State.QUERY
                elif line.endswith('+'):
                    state = State.LINEMERGE
                queries[component_name].append(clear_line(line))
            elif state == State.LINEMERGE:
                if line.endswith(')'):
                    state = State.QUERY
                elif not line.endswith('+'):
                    state = State.STRINGLIST
                queries[component_name][-1] += clear_line(line)
        return queries


def search_for(search_term, filename):
    """Retorna uma lista das queries onde o Termo de Pesquisa foi encontrado"""
    queries = parse_queries_from_dfm(filename)
    found = []
    for k, v in queries.items():
        sql = '\n'.join(v).lower()
        if re.search(r'\b' + search_term + r'\b', sql, flags=re.I):
            found.append(k)
    return found


def search_in_dfm(search_term, filename):
    components = search_for(search_term, filename)
    if components:
        print('Found in "{}":'.format(filename))
        for component in components:
            print('  {}'.format(component))


def search_in_all_dfms(search_term):
    for filename in glob.glob("**/*.dfm", recursive=True):
        search_in_dfm(search_term, filename)


def main():
    if len(sys.argv) < 2:
        print('DFMGrep busca o termo informado em listas de strings dos arquivos .dfm')
        print('')
        print('Uso: dfmgrep [arquivo_dfm] <termo_pesquisado>')
        sys.exit(1)

    if len(sys.argv) == 2:
        search_term = sys.argv[1]
        search_in_all_dfms(search_term)
    elif len(sys.argv) == 3:
        dfm_file = sys.argv[1]
        search_term = sys.argv[2]
        search_in_dfm(search_term, dfm_file)


if __name__ == "__main__":
    main()