"""
Busca uso do termo informado em diversas tabelas
dentro do banco de dados Ello.
"""

import sys
import fdb

# Usa a base de dados de testes
conn = fdb.connect('/ello/dados/testes/TESTE.ELLO')
cursor = conn.cursor()


def busca_termo_em_tdrecontas(search_term):
    cursor.execute(f'''\
    SELECT empresa, idconta
    FROM TDREContas
    WHERE sql CONTAINING '{search_term}'
    ''')
    for empresa, idconta in cursor:
        print(f'Found in table "TDREContas": Empresa={empresa}, IdConta={idconta}')


def busca_termo_em_tgeretiqueta(search_term):
    cursor.execute(f'''\
    SELECT r.IDETIQUETA, r.TABELA
    FROM TGERETIQUETA r
    where r.SQL containing '{search_term}'
    ''')
    for id_etiqueta, tabela in cursor:
        print(f'Found in table "TGerEtiqueta": IdEtiqueta={id_etiqueta}, Tabela={tabela}')


def busca_termo_em_tgerpesquisa(search_term):
    cursor.execute(f'''\
    SELECT r.IDPESQUISA, r.NOME
    FROM TGERPESQUISA r
    WHERE sqlmemo CONTAINING '{search_term}'
    ''')
    for id_pesquisa, nome in cursor:
        print(f'Found in table "TGerPesquisa": IdPesquisa={id_pesquisa}, Nome={nome}')


def busca_termo_em_tplccontafixa(search_term):
    cursor.execute(f'''\
    SELECT r.IDCONTAFIXA, r.DESCRICAO
    FROM TPLCCONTAFIXA r
    WHERE r.SQL CONTAINING '{search_term}'
    ''')
    for id_conta_fixa, descricao in cursor:
        print(f'Found in table "TPLCContaFixa": IdContaFixa={id_conta_fixa}, Descricao={descricao}')
        
        
def main():
    search_term = sys.argv[1]
    busca_termo_em_tdrecontas(search_term)
    busca_termo_em_tgeretiqueta(search_term)
    busca_termo_em_tgerpesquisa(search_term)
    busca_termo_em_tplccontafixa(search_term)
    cursor.close()


if __name__ == "__main__":
    main()