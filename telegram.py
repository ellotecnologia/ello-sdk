#coding: utf8
import os

import telepot
import logging
import config

logger = logging.getLogger()

# -211240257
# @ellotecnologia
def envia_mensagem(mensagem):
    bot = telepot.Bot(config.telegram_token)
    bot.sendMessage('@ellotecnologia', mensagem, parse_mode='Markdown')

def notifica():
    logger.info(u"Notificando suporte via Telegram...")
    mensagem = u"(*Ello*) Nova revisão disponível\n\n"
    # temp.txt é o arquivo criado ao gerar o changelog
    with open('temp.txt') as f:
        mensagem += f.read().decode('latin1')
    mensagem += "\n\n[Changelog](http://wiki.ellotecnologia.net.br/wiki:changelog)"
    os.remove('temp.txt')
    envia_mensagem(mensagem)

if __name__=="__main__":
    notifica()

