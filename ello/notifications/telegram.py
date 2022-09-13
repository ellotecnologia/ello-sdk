import logging

import telepot

from ello.sdk import config

def send_message(mensagem, chat_id):
    mensagem = mensagem.replace("_", "\\_")  # Se não substituir dispara telepot.exception.TelegramError
    bot = telepot.Bot(config.telegram_token)
    bot.sendMessage(chat_id, mensagem, parse_mode='Markdown')


if __name__=="__main__":
    chat_id = '-211240257'  # Chat de testes
    send_message('ProjetoX', chat_id)
