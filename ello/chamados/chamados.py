#!c:/python37/python.exe
import sys
import subprocess
import re
import fdb

from ello.sdk import config

ID_RESPONSAVEL_PADRAO = 17 # MAURICIO

connection = None


class Chamado:
    def __init__(self, cursor):
        self.cursor = cursor


    def finaliza(self, mensagem):
        print("=> Atualizando status do chamado #{0}".format(self.numero))

        if not mensagem:
            self.adiciona_historico("Disponível no próximo release.")
        else:
            self.adiciona_historico(mensagem)

        novo_responsavel = self.idoperador if self.idoperador != self.idresponsavel else ID_RESPONSAVEL_PADRAO
        self.atualiza_responsavel(novo_responsavel)


    def adiciona_historico(self, mensagem):
        idevento = self._obtem_proximo_id_evento()
        self.cursor.execute("INSERT INTO TSolEvento (idevento, empresa, idoperador, descricao, idsolicitacao) VALUES (?, 1, ?, ?, ?)",
                            (idevento, self.idresponsavel, mensagem.encode("latin1"), self.numero))


    def atualiza_responsavel(self, id_responsavel):
        self.cursor.execute("UPDATE TSolSolicitacao SET responsavel=? WHERE idsolicitacao=?", (id_responsavel, self.numero))


    def _obtem_proximo_id_evento(self):
        self.cursor.execute("SELECT MAX(IdEvento)+1 Id "
                            "FROM TSolEvento "
                            "WHERE Empresa=1 AND IdSolicitacao={0}".format(self.numero))
        row = self.cursor.fetchone()
        return (row[0] or 1)


    @staticmethod
    def localiza(numero_chamado):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT IdOperador, Responsavel "
                       "FROM TSolSolicitacao "
                       "WHERE IdSolicitacao={}".format(numero_chamado))
        row = cursor.fetchone()
        if not row:
            return ChamadoNulo(cursor)
        else:
            chamado = Chamado(cursor)
            chamado.numero = numero_chamado
            chamado.idoperador = row[0]
            chamado.idresponsavel = row[1]
            return chamado


class ChamadoNulo(Chamado):
    
    def finaliza(self, mensagem):
        pass


def fecha_chamados_por_mensagem_commit(mensagens: list[str], release: str) -> None:
    connection = get_connection()
    for mensagem in mensagens:
        numeros_chamados = extrai_numeros_chamados(mensagem)
        if not numeros_chamados:
            continue
        for numero_chamado in numeros_chamados:
            chamado = Chamado.localiza(numero_chamado)
            chamado.finaliza('Resolvido no release {}'.format(release))
    connection.commit()


def obtem_msg_ultimo_commit():
    cmd = "git log -1 --format=%s%n%b"
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    return p.communicate()[0].decode("utf8")


def extrai_numeros_chamados(msg_commit):
    """Retorna o número (ou números) de chamados contidos em uma mensagem de commit"""
    match = re.search(r"(?P<ids>\(\#\d+(\, #\d+)*\)?)", msg_commit)
    if match:
        numeros_chamados = match.group('ids')
        return re.findall(r'#(\d+)', numeros_chamados)
    else:
        return None


def get_connection():
    global connection
    if not connection:
        connection = fdb.connect(user=config.firebird_user, password=config.firebird_pass, host=config.firebird_host, database=config.firebird_database)
    return connection


# if __name__ == "__main__":
    # fecha_chamados_por_mensagem_commit(['Chamado concluído (#23291)'], '0.0.0.1')
