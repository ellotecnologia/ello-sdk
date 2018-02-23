# encoding: utf8
""" Sends build notification to the Helpdesk team
"""
import sys
import logging
import telegram
# import whatsapp
# import skype
# import facebook

logging.basicConfig(level=logging.INFO)

def notify_team(project_name):
    # whatsapp.send_notification(project_name)
    # skype.send_notification(project_name)
    # facebook.send_notification(project_name)
    telegram.send_notification(project_name)

if __name__=="__main__":
    notify_team(sys.argv[1])

