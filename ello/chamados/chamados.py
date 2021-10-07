#!c:/python37/python.exe
import sys
import subprocess
import re
import fdb

from ello.sdk import config

ID_RESPONSAVEL = 10
ID_RESPONSAVEL_PADRAO = 5 # GUSTAVO

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
    def localiza(numero_chamado, id_responsavel):
        cursor = obtem_cursor()
        cursor.execute("SELECT IdOperador, Responsavel "
                       "FROM TSolSolicitacao "
                       "WHERE IdSolicitacao={} AND Responsavel={}".format(numero_chamado, ID_RESPONSAVEL))
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


def obtem_msg_ultimo_commit():
    cmd = "git log -1 --format=%s%n%b"
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    return p.communicate()[0].decode("utf8")


def extrai_numero_chamado(msg_commit):
    match = re.search("#(\d+)", msg_commit)
    if match:
        return match.group(1)
    else:
        return None


def obtem_cursor():
    global connection
    if not connection:
        connection = fdb.connect(user=config.firebird_user, password=config.firebird_pass, host=config.firebird_host, database=config.firebird_database)
    return connection.cursor()


def fecha_chamados_por_mensagem_commit(mensagens, release):
    for mensagem in mensagens:
        numero_chamado = extrai_numero_chamado(mensagem)
        if not numero_chamado:
            continue
        chamado = Chamado.localiza(numero_chamado, ID_RESPONSAVEL)
        chamado.finaliza('Resolvido no release {}'.format(release))
        connection.commit()


if __name__ == "__main__":
    msg_commit = obtem_msg_ultimo_commit().split("\n")
    assunto = msg_commit[0]
    mensagem = "\n".join(msg_commit[1:]).strip()

    numero_chamado = extrai_numero_chamado(assunto)
    if not numero_chamado:
        sys.exit()
        
    chamado = Chamado.localiza(numero_chamado, ID_RESPONSAVEL)
    chamado.finaliza(mensagem)
    connection.commit()
