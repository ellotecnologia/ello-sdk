# Ello dev utils

Este projeto contém vários utilitários para facilitar o 
desenvolvimento de projetos [Ello](http://www.ellotecnologia.net.br).

## Utilitários

Nome               | Descrição
-------------------|----------
configure          | Prepara o ambiente (dependencias de pacotes)
make               | Faz o build do projeto, gera changelogs, atualiza resources, faz o deploy para produção
crystal            | Permite pesquisar strings em arquivos .rpt do Crystal Reports. Permite testar queries nos .rpt
emulador_balanca   | Emula uma balança em rede para utilizar em testes
ordena-uses        | Ordena cláusula uses de units Delphi
mass_project_fixer | Efetua modificações em massa em um projeto Delphi (normalmente utilizado em refatorações)


## Dependências

Os executáveis a seguir deverão estar no PATH do computador
que irá realizar o build/release:

 * 7za (utilitário de linha de comandos para compactação)
 * scp (para transferência do executável para o servidor)


## Configuração

O script irá procurar por um arquivo chamado ello-builder.ini
localizado na pasta do usuário (Ex: C:\Users\Fulano\ello-builder.ini)

Exemplo de arquivo de configuração:

```.ini
[servidor]
hostname = 10.1.1.100
ssh_port = 22
ssh_user = username
ssh_key  = mysecret.key

[ftp]
path = /home/ftp/Downloads

[wiki]
user = wiki_user
password = wiki_password

[skype]
group_blob = long_and_boring_skype_blob

[whatsapp]
url = http://10.1.1.100/cgi-bin/zapzap
notify_numbers = 6692380000, 6692330000, 6699020000

[telegram]
token = 000000000:0000000-000000000000000000000000000
```
