PROJECT = {project_name}
VERSION = {project_version}
OUTPUT_DIR = \Ello\Windows 
TARGET = $(OUTPUT_DIR)\$(PROJECT).exe
PACKED_TARGET = $(OUTPUT_DIR)\$(PROJECT)-$(VERSION).zip

DEBUG_FLAGS = -$O- -$W+ -$D+ -$L+ -$Y+ -$C+
RELEASE_FLAGS = -$O+ -$W- -$D- -$L- -$Y- -$C-

RESOURCES = $(PROJECT).res

RESOURCE_FILES = $(PROJECT).rc

all: resources debug 

deploy: release pack send notify

resources: $(RESOURCES)

clean:
	@echo - Removendo arquivos temporários...
	@DEL /S /Q *.dcu >NUL
	@DEL /S /Q *.ddp >NUL
	@DEL /S /Q *.~* >NUL
	@DEL /S /Q *.dsk >NUL

debug:
	@echo - Construindo projeto (DEBUG)...
	@dof debug
	@dcc32 $(DEBUG_FLAGS) -q -b $(PROJECT) >NUL

release: clean resources
	@echo - Construindo projeto (RELEASE)...
	# É preciso atualizar o arquivo .cfg de acordo com o que está no
	# arquivo .dof (para atualizar search paths, etc), mas evitar utilizar
	# a configuração de Conditionals pq o desenvolvedor pode ter colocado
	# diretivas de teste e isto irá afetar o build de release.
	@dof release
	@dcc32 $(RELEASE_FLAGS) -q -b $(PROJECT).dpr >NUL

$(RESOURCES): $(RESOURCE_FILES)
	@echo - Construindo resources...
	@brcc32 resources\$(PROJECT).rc -fo resources\$(PROJECT).res >NUL

changelog:
	@ell bump-version
	@ell make-changelog

notify:
	@ell notify-team
	@ell update-wiki

pack:
	@echo - Empacotando executavel
	@7z a -bd $(PACKED_TARGET) $(TARGET) >NUL

send:
	@echo - Enviando artefatos para o servidor FTP
	@scp $(PACKED_TARGET) server:/home/ftp/Downloads/
