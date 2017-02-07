#coding: utf8
import os
import logging
import telepot

logger = logging.getLogger()
bot = telepot.Bot('207964732:AAF5jGv-pJObNeeEOTkAnFTIisLppF8Imu0')

#pessoas = [
#    128292735, # clayton
#    209495385, # bruno
#    147637406, # erico
#    217182434, # Cristiano
#    203537801, # Henrique
#    209769696, # José Antônio
#    202119638, # Ualisson
#    178499398, # Robson
#    193227964, # Paulão
#]

def envia_mensagem(mensagem):
    bot.sendMessage('@ellotecnologia', mensagem)

def notifica():
    logger.info(u"Notificando suporte via Telegram...")
    mensagem = u"Nova revisão disponível para download\n\n"
    # temp.txt é o arquivo criado ao gerar o changelog
    with open('temp.txt') as f:
        mensagem += f.read().decode('latin1')
    os.remove('temp.txt')
    envia_mensagem(mensagem)

if __name__=="__main__":
    notifica()

# telegram.me/ElloRobot
# Grupo: bot.sendMessage(-137587955, 'Senha do usuario Master em 20/04/2016: 9c94b5')
