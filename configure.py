#coding: utf8
import os
import re
import subprocess
import argparse

def get_revision_from_file(arquivo):
    arquivo.readline()
    return arquivo.readline().split(':')[1].strip()

def checkout_revision(caminho, revisao):
    print u'{0} - Fazendo checkout da revisão {1}'.format(caminho, revisao)
    os.chdir(caminho)
    FNULL = open(os.devnull, 'w')
    command = 'git checkout {0}'.format(revisao).split()
    subprocess.call(command, stdout=FNULL, stderr=subprocess.STDOUT)

def update_requirements():
    with open('LEIAME.txt', 'r') as arquivo_leiame:
        while True:
            linha = arquivo_leiame.readline()

            if not linha:
                break

            if re.match('^Excellent', linha):
                revisao = get_revision_from_file(arquivo_leiame)
                checkout_revision('/dev/componentes/Excellent', revisao)

            #if re.match('^Triburtini', linha):
            #    revisao = get_revision_from_file(arquivo_leiame)
            #    checkout_revision('/dev/componentes/triburtini', revisao)

            if re.match('^ACBr', linha):
                revisao = get_revision_from_file(arquivo_leiame)
                checkout_revision('/dev/componentes/trunk2', revisao)

def freeze_requirements():
    saida = u"""
Excellent
  Repositório : git@bitbucket.org:ellotecnologia/excellent.git
  Revisão     : {0}

ACBr
  Repositório : ssh://git@10.1.1.100:2202/var/repos/acbr-trunk2.git
  Revisão     : {1}
"""
    revisao_excellent  = get_last_commit('/dev/componentes/Excellent')
    #revisao_triburtini = get_last_commit('/dev/componentes/triburtini')
    revisao_acbr       = get_last_commit('/dev/componentes/trunk2')
    print saida.format(
        revisao_excellent,
        #revisao_triburtini,
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

