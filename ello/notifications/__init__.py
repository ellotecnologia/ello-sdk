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


def init_args(args):
    parser = args.add_parser("notify-team", help="Envia notificação de lançamento de revisão para o time")
    parser.set_defaults(func=notify_team)


def notify_team(args):
    project = ProjectMetadata()
    chat_id = '@ellotecnologia'
    #chat_id = '-211240257'  # Chat de testes
    message = telegram.create_message(project)
    logger.info("Notificando time via Telegram...")
    telegram.send_message(message, chat_id)


if __name__=="__main__":
    notify_team()

