# Build Events

Esta extensão da IDE Delphi adiciona um comportamento similar
ao "Visual Studio Build Events".

# Visão Geral

Esta extensão permite executar comandos ou arquivos .bat antes
e depois da compilação do projeto.

Existem dois eventos de build que podem ser configurados:

- pre-build
- post-build

Os comandos **pre-build** são executados sempre que é iniciado
o processo de build do projeto. Isto é útil caso precisemos parar
algum processo ou fazer alguma limpeza antes da compilação.

    Ex: taskkill /im dllhost.exe (ou) simplesmente exibir - echo hello world!

Comandos de **post-build** possuem três eventos:

- Onbuild Success
- OnbuildFailure
- Always Execute


    Ex: copiar artefato gerado para uma pasta específica. Algo como:
    xcopy $(TargetPath)$(TargetFileName) $(TMan)NG\qa\$(TargetFileName) /c /d /f /y

A saída (stdout) do comando executado é exibida na janela "Build Events",
junto com outras mensagens do compilador.

Mensagens na cor verde indicam execução bem sucedida e vermelha indicam
execução mal sucedida. Mensagens em azul são apenas informativas.

# Configuração dos eventos

Para configurar os eventos, acesse o menu do delphi "Project -> Build Events"
e informe os comandos a serem executados na caixa de texto.

Um clique duplo na caixa de texto irá exibir a janela de macros.
