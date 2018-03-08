import config
from pipeline import changelog

def notifica_suporte_via_whatsapp():
    versao = '.'.join(changelog.get_next_tag())
    mensagem = "Nova revisao %s disponivel para download - Ello Tecnologia." % versao
    celular = "556692836044-1446577135" # Grupo Ello
    print 'Notificando %s via WhatsApp...' % celular
    envia_msg_whatsapp(celular, mensagem)

def envia_msg_whatsapp(numero_celular, mensagem):
    import requests
    #numero_celular = "55" + numero_celular
    payload = {'fone': numero_celular, 'msg': mensagem}
    r = requests.get(config.whatsapp_url, params=payload)

