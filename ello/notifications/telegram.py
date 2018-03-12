#coding: utf8
import os
import logging

import telepot
from ello.sdk import config

logger = logging.getLogger()

TMP_CHANGELOG_FILE = os.environ.get('TEMP') + '\\ell_changelog.tmp'

# -211240257
# @ellotecnologia
def send_message(mensagem):
    bot = telepot.Bot(config.telegram_token)
    bot.sendMessage('@ellotecnologia', mensagem, parse_mode='Markdown')

def send_notification(project_name):
    logger.info(u"Notificando time via Telegram...")
    mensagem = u"(*{0}*) Nova revisão disponível\n\n".format(project_name)
    with open(TMP_CHANGELOG_FILE) as f:
        mensagem += f.read().decode('latin1')
    mensagem += "\n[Changelog](http://wiki.ellotecnologia.net.br/wiki:changelog:{0})".format(project_name)
    send_message(mensagem)

if __name__=="__main__":
    send_notification()

