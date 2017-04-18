#coding: utf8
import os
import re
import subprocess
import argparse

PASTA_COMPONENTES = os.getenv('COMPONENTES')

def get_revision_from_file(arquivo):
    arquivo.readline()
    return arquivo.readline().split(':')[1].strip()

def checkout_revision(package_name, revision_hash):
    print u'=> Atualizando {0} ({1})'.format(package_name, revision_hash[0:7])
    os.chdir("{0}/{1}".format(PASTA_COMPONENTES, package_name))
    FNULL = open(os.devnull, 'w')
    command = 'git checkout {0}'.format(revision_hash).split()
    return_code = subprocess.call(command, stdout=FNULL, stderr=subprocess.STDOUT)

    # Se der erro ao fazer o checkout da revisão, tenta fazer um fetch e fazer o checkout novamente
    if return_code!=0:
        fetch_reporitory('excellent')
        subprocess.call(command, stdout=FNULL, stderr=subprocess.STDOUT)

def fetch_reporitory(package_name):
    print "Fazendo fetch do repositorio", package_name
    FNULL = open(os.devnull, 'w')
    os.chdir(PASTA_COMPONENTES + '/' + package_name)
    subprocess.call('git fetch', stdout=FNULL, stderr=subprocess.STDOUT)

def update_requirements():
    with open('LEIAME.txt', 'r') as arquivo_leiame:
        while True:
            linha = arquivo_leiame.readline()

            if not linha:
                break

            if re.match('^Excellent', linha):
                revisao = get_revision_from_file(arquivo_leiame)
                checkout_revision('excellent', revisao)

            if re.match('^ACBr', linha):
                revisao = get_revision_from_file(arquivo_leiame)
                checkout_revision('trunk2', revisao)

def freeze_requirements():
    saida = u"""
Excellent
  Repositório : git@bitbucket.org:ellotecnologia/excellent.git
  Revisão     : {0}

ACBr
  Repositório : ssh://git@10.1.1.100:2202/var/repos/acbr-trunk2.git
  Revisão     : {1}
"""
    revisao_excellent  = get_last_commit('{0}/Excellent'.format(PASTA_COMPONENTES))
    revisao_acbr       = get_last_commit('{0}/trunk2'.format(PASTA_COMPONENTES))
    print saida.format(
        revisao_excellent,
        revisao_acbr
    )

def get_last_commit(path):
    os.chdir(path)
    FNULL = open(os.devnull, 'w')
    command = 'git log -1 --pretty=format:%H'
    git = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    out, err = git.communicate()
    return out

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Ello Requirements management tool')
    parser.add_argument('--freeze', action="store_true", default=False)
    args = parser.parse_args()

    if args.freeze:
        freeze_requirements()
    else:
        update_requirements()

