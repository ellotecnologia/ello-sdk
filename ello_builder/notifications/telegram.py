#coding: utf8
import logging

import telepot
from ello_builder import config

logger = logging.getLogger()

# -211240257
# @ellotecnologia
def send_message(mensagem):
    bot = telepot.Bot(config.telegram_token)
    bot.sendMessage('@ellotecnologia', mensagem, parse_mode='Markdown')

def send_notification(project_name):
    logger.info(u"Notificando time via Telegram...")
    mensagem = u"(*{0}*) Nova revisão disponível\n\n".format(project_name)
    # temp.txt é o arquivo criado ao gerar o changelog
    with open('temp.txt') as f:
        mensagem += f.read().decode('latin1')
    mensagem += "\n[Changelog](http://wiki.ellotecnologia.net.br/wiki:changelog:{0})".format(project_name)
    send_message(mensagem)

if __name__=="__main__":
    send_notification()

