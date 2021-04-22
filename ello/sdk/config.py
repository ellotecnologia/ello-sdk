import os
import os.path
from configparser import ConfigParser

config_filename = os.path.join(os.path.expanduser('~'), 'ello-sdk.ini')

config = ConfigParser()
config.read(config_filename)

hostname = config.get('servidor', 'hostname', fallback='server')
ssh_port = config.get('servidor', 'ssh_port', fallback='2202')
ssh_user = config.get('servidor', 'ssh_user', fallback='user')
ssh_key  = config.get('servidor', 'ssh_key', fallback='id_rsa')

wiki_user = config.get('wiki', 'user', fallback='')
wiki_password = config.get('wiki', 'password', fallback='')

whatsapp_url     = config.get('whatsapp', 'url', fallback='')
whatsapp_numbers = [n.strip() for n in config.get('whatsapp', 'notify_numbers', fallback='').split(',')]
telegram_token = config.get('telegram', 'token', fallback='')

