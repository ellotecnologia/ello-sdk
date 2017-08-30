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

Um arquivo de exemplo chamado ello-builder.sample.ini está
disponível neste projeto.

