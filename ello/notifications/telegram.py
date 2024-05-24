import logging
import re

import telepot

from ello.sdk import config

WIKI_URL = 'https://wiki.ellotecnologia.com'
OS_URL = 'https://os.ellotecnologia.net.br/chamados/'


def send_message(mensagem, chat_id):
    mensagem = mensagem.replace("_", "\\_")  # Se não substituir dispara telepot.exception.TelegramError
    bot = telepot.Bot(config.telegram_token)
    bot.sendMessage(chat_id, mensagem, parse_mode='Markdown', disable_web_page_preview=True)


def create_message(project):
    # Adiciona links nos números de chamado
    changelog = re.sub(r'\(#(\d+)\)', r'([#\1](' + OS_URL + r'\1))', project.texto_ultima_revisao())

    # Adiciona links para o telegram dos autores
    changelog = _create_authors_link(changelog)
    
    message = "\U0001f3c1 Nova revisão disponível \U0001f3c1\n\n"
    message += "*{0}*\n\n".format(project.name)
    
    message += changelog
    message += "\n[Clique aqui para ver histórico completo]({0}/wiki:changelog:{1})".format(WIKI_URL, project.name)
    
    message = _add_telegram_emojis(message)

    return message


def _create_authors_link(changelog):
    tmpl = '<[{}](https://t.me/{})>'
    changelog = re.sub(r'<Clayton>',    tmpl.format('Clayton',    'claytonaalves'),  changelog, flags=re.I)
    changelog = re.sub(r'<Triburtini>', tmpl.format('Triburtini', 'Triburtini'),     changelog, flags=re.I)
    changelog = re.sub(r'<.*Wender.*>', tmpl.format('Wender',     'RWENDER'),        changelog, flags=re.I)
    changelog = re.sub(r'<Bruno.*>',    tmpl.format('Bruno',      '+5511934733404'), changelog, flags=re.I)
    changelog = re.sub(r'<Gustavo.*>',  tmpl.format('Gustavo',    '+5566992524681'), changelog, flags=re.I)
    changelog = re.sub(r'<Lucas.*>',    tmpl.format('Lucas',      'Lucas_Benetti'),  changelog, flags=re.I)
    return changelog


def _add_telegram_emojis(text):
    RED_CIRCLE = '\U0001F534'
    YELLOW_CIRCLE = '\U0001F7E1'
    GREEN_CIRCLE = '\U0001F7E2'
    WHITE_CIRCLE = '\u26AA'
    lines = []
    for line in text.splitlines():
        if line.startswith('- Corr'):
            line = re.sub('^-', RED_CIRCLE, line)
        else:
            line = re.sub('^-', GREEN_CIRCLE, line)
        lines.append(line)
    return '\n'.join(lines)


if __name__=="__main__":
    chat_id = '-211240257'  # Chat de testes
    send_message('ProjetoX', chat_id)
