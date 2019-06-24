import glob
import fileinput
 
def arruma_ebcliente(arquivo):
    dentro_ebcliente = False
    for linha in fileinput.input(arquivo, inplace=True):
        if dentro_ebcliente:
            if linha.strip() == 'end':
                dentro_ebcliente = False
            if 'Properties.MaxLength' in linha:
                linha = linha.replace('= 5', '= 7')
        
        if 'object EBCliente:' in linha:
           dentro_ebcliente = True
        
        print(linha, end='')
            
 
#arruma_ebcliente('Financeiro/Receber/REC400AA.dfm')
for arquivo in glob.glob('**/*.dfm', recursive=True):
    print(arquivo)
    arruma_ebcliente(arquivo)