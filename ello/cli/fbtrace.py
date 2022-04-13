import threading
import queue
import fdb
import argparse

import colorama
colorama.init()

import sqlparse
from pygments import highlight
from pygments.lexers import SqlLexer
from pygments.formatters import Terminal256Formatter
from pygments.style import Style
from pygments.token import Token

class MyStyle(Style):
    styles = {
        Token.String: 'ansigreen bg:ansiblack',
        Token.Keyword: 'ansiblue bg:ansiblack',
        Token.Number: 'ansired'
    }

lexer = SqlLexer()
formatter = Terminal256Formatter(style=MyStyle)

q = queue.Queue()

def firebird_trace():
    svc = fdb.services.connect(password='masterkey', host='localhost')
    trace_config = """
    <database>
        enabled	true
        log_statement_start	true
        log_statement_finish true
        time_threshold 0
        print_plan true
        print_perf true
        max_sql_length 8192
    </database>
    """
    trace_id = svc.trace_start(trace_config, 'test_trace_2')
    sql_statement = []
    inside_statement = False
    while 1:
        try:
           line = svc._QS(fdb.ibase.isc_info_svc_line)
        except fdb.OperationalError:
           break
        if not line: # end of output
           break
        
        #print '>>>>>>>', line
        
        if line.startswith('Statement'):
            inside_statement = True
            sql_statement = []
            continue

        if line.startswith('---------'):
            continue

        if line.startswith('^^^^^^') or ('EXECUTE_STATEMENT_FINISH' in line):
            q.put('\n'.join(sql_statement))
            sql_statement = []
            inside_statement = False

        if inside_statement:
            sql_statement.append(line.strip())


def init_trace_thread():
    t = threading.Thread(target=firebird_trace)
    t.daemon = True
    t.start()


def save_to_file(filename, output):
    with open(filename, 'a') as f:
        f.write(output)
        f.write("\n\n-- ---------------------------\n\n")


def main_loop(args):
    statement_count = 0
    while True:
        try:
            sql = q.get(False, 1)
        except queue.Empty:
            continue
        output = sqlparse.format(sql, reindent=True, keyword_case='upper')

        if args.output_file:
            save_to_file(args.output_file, output)

        output = highlight(output, lexer, formatter)
        print(output)

        print('-- --------------------')
        statement_count += 1
        print('Instrucoes executadas: {}'.format(statement_count))
        print('-- --------------------\n')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--output-file', nargs='?', help="Nome do arquivo para gravar a saida")
    return parser.parse_args()


def main():
    args = parse_args()
    init_trace_thread()
    print('Firebird Trace iniciado\n')
    try:
        main_loop(args)
    except KeyboardInterrupt:
        print('Firebird Trace finalizado')


if __name__ == "__main__":
    main()
