#coding: utf8
import os
import os.path
import re
import subprocess
import argparse
import json
import collections

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
    print(u'=> Coletando metadados do projeto')
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
    with open('package.json', 'r') as f:
        package_info = json.load(f, object_pairs_hook=collections.OrderedDict)

    package_info['dependencies']['excellent'] = obtem_ultimo_commit('{0}/Excellent'.format(PASTA_COMPONENTES))
    package_info['dependencies']['trunk2'] = obtem_ultimo_commit('{0}/trunk2'.format(PASTA_COMPONENTES))
    if package_info['dependencies'].has_key('ello'):
        package_info['dependencies']['ello'] = obtem_ultimo_commit('{0}/ello'.format(PASTA_PROJETO_ELLO))

    with open('package.json', 'w') as f:
        f.write(json.dumps(package_info, indent=2))

def extrai_hash_do_pacote(arquivo):
    arquivo.readline()
    return arquivo.readline().split(':')[1].strip()

def checkout_pacote(nome_pacote, caminho, novo_hash):
    os.chdir("{0}/{1}".format(caminho, nome_pacote))
    if not (copia_de_trabalho_limpa()):
        print(u"Existem modificações não commitadas na pasta {0}\\{1}. Cancelando atualização.".format(caminho, nome_pacote))
        return
    if novo_hash==obtem_hash_atual():
        return
    print(u'=> Atualizando {0} para a revisão {1}'.format(nome_pacote, novo_hash[0:7]))
    command = 'git checkout {0}'.format(novo_hash).split()
    return_code = subprocess.call(command, stdout=FNULL, stderr=subprocess.STDOUT)

    # Se der erro ao fazer o checkout da revisão, tenta fazer um fetch e fazer o checkout novamente
    if return_code!=0:
        baixa_atualizacoes_do_repositorio(nome_pacote)
        subprocess.call(command, stdout=FNULL, stderr=subprocess.STDOUT)

def obtem_hash_atual():
    """ Obtem o hash do último commit no repositório atual
    """
    command = 'git log -1 --pretty="%H"'
    git = subprocess.Popen(command, stdout=subprocess.PIPE)
    return unicode(git.communicate()[0].strip())

def copia_de_trabalho_limpa():
    return_code = subprocess.call("git diff-index --quiet HEAD --", stdout=FNULL, stderr=subprocess.STDOUT)
    return return_code==0

def baixa_atualizacoes_do_repositorio(nome_pacote):
    print("Fazendo fetch do repositorio {0}".format(nome_pacote))
    os.chdir(PASTA_COMPONENTES + '/' + nome_pacote)
    subprocess.call('git fetch', stdout=FNULL, stderr=subprocess.STDOUT)

def obtem_ultimo_commit(caminho):
    curdir = os.getcwd()
    os.chdir(caminho)
    command = 'git log -1 --pretty=format:%H'
    git = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    out, err = git.communicate()
    os.chdir(curdir)
    return out

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Ferramenta de gerenciamento de dependencias de pacotes Ello')
    parser.add_argument('--save', action="store_true", default=False)
    args = parser.parse_args()

    if args.save:
        congela_dependencias()
    else:
        atualiza_dependencias()

