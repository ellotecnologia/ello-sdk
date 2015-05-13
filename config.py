#coding: utf8
import os
from ConfigParser import ConfigParser

user_folder = os.path.expanduser("~")
config_filename = "{}\\ello-builder.ini".format(user_folder)

config = ConfigParser()
config.read(config_filename)

hostname = config.get('servidor', 'hostname')
ssh_port = config.get('servidor', 'ssh_port')
ssh_user = config.get('servidor', 'ssh_user')
ssh_key  = config.get('servidor', 'ssh_key')

ftp_path = config.get('ftp', 'path')

wiki_user = config.get('wiki', 'user')
wiki_password = config.get('wiki', 'password')

