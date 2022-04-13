# encoding: utf8
""" Sends build notification to the Helpdesk team
"""
import sys
import logging

from ello.notifications import telegram
from ello.project import ProjectMetadata

# import whatsapp
# import skype
# import facebook

logging.basicConfig(level=logging.INFO)


def init_args(args):
    parser = args.add_parser("notify-team", help="Envia notificação de lançamento de revisão para o time")
    parser.set_defaults(func=lambda args: notify_team(ProjectMetadata().name))


def notify_team(project_name):
    # whatsapp.send_notification(project_name)
    # skype.send_notification(project_name)
    # facebook.send_notification(project_name)
    telegram.send_notification(project_name)


if __name__=="__main__":
    notify_team(sys.argv[1])
