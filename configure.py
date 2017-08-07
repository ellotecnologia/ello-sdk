#coding: utf8
import os
import os.path
import re
import subprocess
import argparse
import json

PASTA_COMPONENTES = os.getenv('COMPONENTES')
PASTA_PROJETO_ELLO = PASTA_COMPONENTES + "\\.." 
FNULL = open(os.devnull, 'w')

def atualiza_dependencias():
    """ Faz checkout das revisões contidas no arquivo LEIAME.txt ou package.json
    """
    if os.path.isfile('package.json'):
        atualiza_dependencias_package_json()
    else:
        atualiza_dependencias_modo_retrocompatibilidade()

def atualiza_dependencias_package_json():
    print(u'Coletando informações do arquivo package.json')
    with open('package.json', 'r') as json_file:
        package_info = json.load(json_file)
    dependencies = package_info['dependencies']
    for dependency in dependencies:
        nome_pacote = dependency
        codigo_hash = dependencies[dependency]
        if re.match('ello', nome_pacote, re.I):
            checkout_pacote(nome_pacote, PASTA_PROJETO_ELLO, codigo_hash)
        else:
            checkout_pacote(nome_pacote, PASTA_COMPONENTES, codigo_hash)

def atualiza_dependencias_modo_retrocompatibilidade():
    """ Modo de retrocompatibilidade para funcionar com revisões antigas
    """
    with open('LEIAME.txt', 'r') as arquivo_leiame:
        while True:
            linha = arquivo_leiame.readline()
            if not linha:
                break
            if re.match('^Excellent', linha):
                codigo_hash = extrai_hash_do_pacote(arquivo_leiame)
                checkout_pacote('excellent', PASTA_COMPONENTES, codigo_hash)
            if re.match('^ACBr', linha):
                codigo_hash = extrai_hash_do_pacote(arquivo_leiame)
                checkout_pacote('trunk2', PASTA_COMPONENTES, codigo_hash)
            if re.match('^PngComponents', linha):
                codigo_hash = extrai_hash_do_pacote(arquivo_leiame)
                checkout_pacote('PngComponents', PASTA_COMPONENTES, codigo_hash)
            if re.match('^Ello', linha):
                codigo_hash = extrai_hash_do_pacote(arquivo_leiame)
                checkout_pacote('ello', PASTA_PROJETO_ELLO, codigo_hash)

def congela_dependencias():
    saida = u"""
Excellent
  Repositório : git@bitbucket.org:ellotecnologia/excellent.git
  Revisão     : {0}

ACBr
  Repositório : ssh://git@10.1.1.100:2202/var/repos/acbr-trunk2.git
  Revisão     : {1}
"""
    revisao_excellent  = obtem_ultimo_commit('{0}/Excellent'.format(PASTA_COMPONENTES))
    revisao_acbr       = obtem_ultimo_commit('{0}/trunk2'.format(PASTA_COMPONENTES))
    print saida.format(
        revisao_excellent,
        revisao_acbr
    )

def extrai_hash_do_pacote(arquivo):
    arquivo.readline()
    return arquivo.readline().split(':')[1].strip()

def checkout_pacote(nome_pacote, caminho, hash_revisao):
    print u'=> Atualizando {0} ({1})'.format(nome_pacote, hash_revisao[0:7])
    os.chdir("{0}/{1}".format(caminho, nome_pacote))
    if not (copia_de_trabalho_limpa()):
        print u"Existem modificações não commitadas na pasta {0}\\{1}. Cancelando atualização.".format(caminho, nome_pacote)
        return
    command = 'git checkout {0}'.format(hash_revisao).split()
    return_code = subprocess.call(command, stdout=FNULL, stderr=subprocess.STDOUT)

    # Se der erro ao fazer o checkout da revisão, tenta fazer um fetch e fazer o checkout novamente
    if return_code!=0:
        baixa_atualizacoes_do_repositorio(nome_pacote)
        subprocess.call(command, stdout=FNULL, stderr=subprocess.STDOUT)

def copia_de_trabalho_limpa():
    return_code = subprocess.call("git diff-index --quiet HEAD --", stdout=FNULL, stderr=subprocess.STDOUT)
    return return_code==0

def baixa_atualizacoes_do_repositorio(nome_pacote):
    print "Fazendo fetch do repositorio", nome_pacote
    os.chdir(PASTA_COMPONENTES + '/' + nome_pacote)
    subprocess.call('git fetch', stdout=FNULL, stderr=subprocess.STDOUT)

def obtem_ultimo_commit(caminho):
    os.chdir(caminho)
    command = 'git log -1 --pretty=format:%H'
    git = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    out, err = git.communicate()
    return out

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Ferramenta de gerenciamento de dependencias de pacotes Ello')
    parser.add_argument('--freeze', action="store_true", default=False)
    args = parser.parse_args()

    if args.freeze:
        congela_dependencias()
    else:
        atualiza_dependencias()

