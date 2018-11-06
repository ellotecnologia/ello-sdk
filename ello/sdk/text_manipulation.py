# encoding: utf8
from __future__ import unicode_literals
from __future__ import print_function

import re

def preprocess_commit_messages(messages):
    messages = map(remove_unnecessary_characters, messages)
    messages = map(lambda text: re.sub('^(.+) - (.+) (<\w+>)$', '\\2 (\\1) \\3', text, flags=re.I), messages)
    messages = map(translate_personal_verbs, messages)
    messages = map(apply_some_fixups, messages)
    messages = filter(lambda x: not ignore_line(x), messages)
    messages = sorted(messages, cmp=compara)
    messages = map(lambda text: '- ' + text, messages)
    return messages


def remove_unnecessary_characters(text):
    """
    Remover qualquer caracter que não for letra do início da mensagem
    Remover "." do final
    """
    text = text.strip()
    text = re.sub('\.$', '', text)
    text = re.sub('^[^\w]', '', text)
    text = re.sub('^[\d]', '', text)
    text = text.strip()
    return text
    
    
def translate_personal_verbs(text):
    """
    Tornar mensagem impessoal
    """
    text = re.sub('^melhorei', 'Melhorado', text, flags=re.I)
    text = re.sub('^aprimorei', 'Aprimorado', text, flags=re.I)
    text = re.sub('^modifiquei', 'Modificado', text, flags=re.I)
    text = re.sub('^desativei', 'Desativado', text, flags=re.I)
    text = re.sub('^ajustei', 'Ajustado', text, flags=re.I)
    text = re.sub('^implementei', 'Implementado', text, flags=re.I)
    text = re.sub('^criei', 'Criado', text, flags=re.I)
    text = re.sub('^adicionei', 'Adicionado', text, flags=re.I)
    text = re.sub('^inseri', 'Inserido', text, flags=re.I)
    text = re.sub('^coloquei', 'Colocado', text, flags=re.I)
    text = re.sub('^removi\b', 'Removido', text, flags=re.I)
    text = re.sub('^exclu[íi]', 'Removido', text, flags=re.I)
    text = re.sub('^retirei', 'Retirado', text, flags=re.I)
    text = re.sub('^corrigi\b', 'Corrigido', text, flags=re.I)
    text = re.sub('^alterei', 'Alterado', text, flags=re.I)
    text = re.sub('^otimizei', 'Otimizado', text, flags=re.I)
    text = re.sub('^programei', 'Programado', text, flags=re.I)
    text = re.sub('^organizei', 'Organizado', text, flags=re.I)
    text = re.sub('^refatorei', 'Refatorado', text, flags=re.I)
    return text


def apply_some_fixups(text):
    """
    Remove alguns hábitos de elaboração de mensagens
    """
    # Corrige mania do Bruno de colar o número do chamado a mensagem
    text = re.sub('(\w|\d)\(#', '\\1 (#', text)
    
    # Corrige algumas manias do Paulinho
    text = re.sub('pequen(o|a) (ajust.|corre..o|mudan.a)', 'Correção', text, flags=re.I)
    text = re.sub('um correção', 'uma correção', text, flags=re.I)
    text = re.sub('ajust(e|ei|ado) (no|na|para)', 'Aprimoramento \\2', text, flags=re.I)
    text = re.sub('refatur(ar|ei|ado)', 'refator\\1', text, flags=re.I)
    text = re.sub('program(ei|ado) para', 'Aprimoramento para', text, flags=re.I)
    text = re.sub('modifi(quei|cado) para', 'Aprimoramento para', text, flags=re.I)
    text = re.sub('implement(ei|ado) para', 'Aprimoramento para', text, flags=re.I)

    # Corrige algumas manias de todo programador
    text = re.sub('(na|no) grid', 'na grade', text, flags=re.I)
    text = re.sub('no form ', 'na tela ', text, flags=re.I)
    text = re.sub('o form ', 'a tela ', text, flags=re.I)
    text = re.sub('melhor(ei|ia|ado) (o|a|no|na|para)', 'Aprimoramento \\2', text, flags=re.I)
    text = re.sub('melhoria', 'Aprimoramento', text, flags=re.I)
    text = re.sub('aprimoramento a', 'Aprimoramento na', text, flags=re.I)
    text = re.sub('aprimoramento o', 'Aprimoramento no', text, flags=re.I)
    text = re.sub('otimiza..o (no|na|para)', 'Aprimoramento \\1', text, flags=re.I)
    text = re.sub('reestrutura..o (no|na)', 'Aprimoramento \\1', text, flags=re.I)

    text = re.sub('^(ajustado (o|a)*)', 'Aprimoramento: \\1', text, flags=re.I)
    text = re.sub('^(alterado (o|a|para))', 'Aprimoramento: \\1', text, flags=re.I)
    text = re.sub('^(removido (o|a)*)', 'Aprimoramento: \\1', text, flags=re.I)
    text = re.sub('^(adicionado (o|a)*)', 'Aprimoramento: \\1', text, flags=re.I)
    text = re.sub('^(coloquei (o|a|os|as|um|uma)*)', 'Aprimoramento: \\1', text, flags=re.I)
    text = re.sub('^(criado (o|a|os|as|um|uma)*)', 'Aprimoramento: \\1', text, flags=re.I)
    
    text = text[0].upper() + text[1:]
    return text

    
def ignore_line(text):
    """ Ignorar mensagem caso ela possua algum termo técnico
    """
    technical_terms = []
    
    technical_terms.append('review(s*)')
    technical_terms.append('^revis(a|ã)o')
    technical_terms.append('metadado(s*)')
    technical_terms.append('refator(ei|ado|ada|ação)')
    technical_terms.append('compila(r|ado|ando|ção|cao)')
    technical_terms.append('c.digo fonte')
    technical_terms.append('desacopla(ando|ado)*')
    technical_terms.append('removi(do|da)* (m.todo|rotina|atributo|propriedade)')
    technical_terms.append('renome(ado|ada|ei) vari.vel')
    technical_terms.append('organiz(ando|ei) (m.todo|rotina|atributo|propriedade)(s)*')
    technical_terms.append('transformei (rotina|função|funcao)')
    technical_terms.append('changelog')
    technical_terms.append('projeto(s)* de teste')
    
    technical_terms.append(r'thread(s)*')
    technical_terms.append(r'\bunit(s)*\b')
    technical_terms.append(r'\buse(s)*\b')
    technical_terms.append(r'warning(s)*')
    technical_terms.append(r'\bhint(s)*\b')
    technical_terms.append(r'\blabel(s)*\b')
    technical_terms.append(r'string(s)*')
    technical_terms.append(r'panel(s)*')
    technical_terms.append(r'\bacbr\b')
    technical_terms.append(r'\bindy\b')
    technical_terms.append(r'excellent')
    technical_terms.append(r'\bform(s)*\b')
    technical_terms.append(r'makefile')
    technical_terms.append(r'\b(client)*dataset\b')
    technical_terms.append(r'\bcombobox\b')
    technical_terms.append(r'\btabsheet\b')
    technical_terms.append(r'\bframe\b')
    technical_terms.append(r'\bresource(s)*\b')
    
    technical_terms.append(r'trigger(s)*')
    technical_terms.append(r'procedure(s)*')
    technical_terms.append(r'view(s)*')
    
    technical_terms.append(r'merge(s)*')
    technical_terms.append(r'branch(s|es)*')
    technical_terms.append(r'commit(s)*')
    technical_terms.append(r'\brevert\b')

    return bool(re.search('(' + '|'.join(technical_terms) + ')', text, flags=re.I))


def compara(a, b):
    a = a.lower()[0:5]
    b = b.lower()[0:5]
    if a == b:
        return 0

    if (a == 'imple'):
        return -10
    if (b == 'imple'):
        return 10
        
    if (a == 'adici'):
        return -9
    if (b == 'adici'):
        return 9

    if (a == 'aprim'):
        return -8
    if (b == 'aprim'):
        return 8
        
    if (a == 'corre'):
        return -7
    if (b == 'corre'):
        return 7
        
    if (a == 'corri'):
        return -6
    if (b == 'corri'):
        return 6
        
    return cmp(a, b)
    

if __name__=='__main__':
    mensagens = """\
Aprimoramento na função Capitalize
Aprimoramento do instalador para perguntar nome do banco apenas se for instalar o banco de dados
Correção na gravação dos lotes de produtos controlados (#9133)
Correção no carregamento dos parâmetros do SNGPC
Retirado do menu principal programas obsoletos (Plano de Contas)
Atualização do changelog (1.2.56.168)
""".splitlines()    
    mensagens = preprocess_commit_messages(mensagens)
    for mensagem in mensagens:
        print(mensagem)