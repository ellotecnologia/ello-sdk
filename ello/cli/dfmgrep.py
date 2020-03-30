import sys
import re
import glob
from enum import Enum
from collections import defaultdict

RE_QUERY = re.compile('object (\w+): TSQLQuery')

class State(Enum):
    OUTER = 1
    QUERY = 2
    STRINGLIST = 3
    LINEMERGE = 4


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
    query_name = ''
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
                    query_name = match.group(1)
                    state = State.QUERY
            elif state == State.QUERY:
                if line == 'end':
                    state = State.OUTER
                elif 'SQL.Strings' in line:
                    state = State.STRINGLIST
            elif state == State.STRINGLIST:
                if line.endswith(')'):
                    state = State.QUERY
                elif line.endswith('+'):
                    state = State.LINEMERGE
                queries[query_name].append(clear_line(line))
            elif state == State.LINEMERGE:
                if line.endswith(')'):
                    state = State.QUERY
                elif not line.endswith('+'):
                    state = State.STRINGLIST
                queries[query_name][-1] += clear_line(line)
        return queries


def search_for(search_term, filename):
    """Retorna uma lista das queries onde o Termo de Pesquisa foi encontrado"""
    queries = parse_queries_from_dfm(filename)
    found = []
    for k, v in queries.items():
        sql = '\n'.join(v).lower()
        if re.search(r'\b' + search_term + r'\b', sql):
            found.append(k)
    return found


def search_in_dfm(search_term, filename):
    result = search_for(search_term, filename)
    if result:
        print('Found in "{}". Queries: {}'.format(filename, ', '.join(result)))


def main():
    if len(sys.argv) < 2:
        print('Uso: dfmgrep [termo_pesquisado]')
        sys.exit(1)
    search_term = sys.argv[1]
    for filename in glob.glob("**/*.dfm", recursive=True):
        search_in_dfm(search_term, filename)


if __name__ == "__main__":
    main()