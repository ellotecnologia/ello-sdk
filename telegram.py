#coding: utf8
import os
import logging
import telepot

import config

logger = logging.getLogger()

def envia_mensagem(mensagem):
    bot = telepot.Bot(config.telegram_token)
    bot.sendMessage('@ellotecnologia', mensagem)

def notifica():
    logger.info(u"Notificando suporte via Telegram...")
    mensagem = u"Nova revisão disponível para download\n\n"
    # temp.txt é o arquivo criado ao gerar o changelog
    with open('temp.txt') as f:
        mensagem += f.read().decode('latin1')
    mensagem += "\n\nhttp://wiki.ellotecnologia.net.br/wiki:changelog"
    os.remove('temp.txt')
    envia_mensagem(mensagem)

if __name__=="__main__":
    notifica()

