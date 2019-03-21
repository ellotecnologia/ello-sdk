# encoding: utf8
from __future__ import unicode_literals

import os
import logging
import re

import telepot

from ello.sdk import config

logger = logging.getLogger()

chat_id = '@ellotecnologia'
WIKI_URL = 'http://wiki.ellotecnologia.net.br'


def send_notification(project_name):
    logger.info("Notificando time via Telegram...")
    mensagem = "\U0001f3c1 Nova revisão disponível \U0001f3c1\n\n"
    mensagem += "*{0}*\n\n".format(project_name)
    mensagem += get_changelog_text()
    mensagem += "\n[Clique aqui para ver histórico completo]({0}/wiki:changelog:{1})".format(WIKI_URL, project_name)
    send_message(mensagem)    


def get_changelog_text():
    changelog = os.environ.get('TEMP') + '\\ell_changelog.tmp'
    with open(changelog) as f:
        text = f.read().decode('latin1')
    text = add_emojis(text)
    return text


def add_emojis(text):
    lines = []
    for line in text.splitlines():
        if line.startswith('- Corr'):
            #line = re.sub('^-', '\U0001f41e', line)
            line = re.sub('^-', '\u26a0\ufe0f', line)
        elif line.startswith('- Adic'):
            line = re.sub('^-', '\u2728', line)
        elif line.startswith('- Impl'):
            line = re.sub('^-', '\U0001f525', line)
        else:
            line = re.sub('^-', '\u2728', line)
        lines.append(line)
    return '\n'.join(lines)


def send_message(mensagem):
    mensagem = mensagem.replace("_", "\\_")  # Se não substituir dispara telepot.exception.TelegramError
    bot = telepot.Bot(config.telegram_token.encode('utf8'))
    bot.sendMessage(chat_id.encode('utf8'), mensagem.encode('utf8'), parse_mode='Markdown')


if __name__=="__main__":
    chat_id = '-211240257'  # Chat de testes
    #send_message('Teste com acentuação!')
    send_notification('ProjetoX')
