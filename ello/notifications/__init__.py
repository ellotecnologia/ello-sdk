# encoding: utf8
""" Sends build notification to the Helpdesk team
"""
import sys
import logging
import re

from ello.notifications import telegram
from ello.project import ProjectMetadata

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()

WIKI_URL = 'http://wiki.ellotecnologia.net.br'


def init_args(args):
    parser = args.add_parser("notify-team", help="Envia notificação de lançamento de revisão para o time")
    parser.set_defaults(func=notify_team)


def notify_team(args):
    project = ProjectMetadata()
    chat_id = '@ellotecnologia'
    #chat_id = '-211240257'  # Chat de testes
    message = _create_telegram_message(project)
    message = _add_telegram_emojis(message)
    logger.info("Notificando time via Telegram...")
    telegram.send_message(message, chat_id)


def _create_telegram_message(project):
    message = "\U0001f3c1 Nova revisão disponível \U0001f3c1\n\n"
    message += "*{0}*\n\n".format(project.name)
    message += project.texto_ultima_revisao()
    message += "\n[Clique aqui para ver histórico completo]({0}/wiki:changelog:{1})".format(WIKI_URL, project.name)
    return message


def _add_telegram_emojis(text):
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


if __name__=="__main__":
    notify_team()
