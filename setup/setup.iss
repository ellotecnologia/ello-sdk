; TODO: estou considerando adicionar no SDK os seguintes programas:
;   CodeCoverage, DbgView, diff-pdf, nc, ResourceHacker, XSDDiagram

; TODO: Instalar python 3
; python-3.9.0.exe /passive InstallAllUsers=1 PrependPath=1 Include_test=0

#define MyAppName "Ello SDK"
#define MyAppVersion "1.0"
#define MyAppPublisher "Ello tecnologia"
#define MyAppURL "http://www.ellotecnologia.com/"

[Setup]
AppId={{20F19583-E410-47CE-921E-D239BDA26798}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName=C:\bin
DisableDirPage=yes
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=dist
OutputBaseFilename=Ello-SDK-{#MyAppVersion}
Compression=lzma
SolidCompression=yes
ChangesEnvironment=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Files]
Source: "bin\dof2cfg.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "bin\fd.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "bin\rg.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "bin\configure.exe"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Code]
const
  ENVIRONMENT_KEY = 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment';

function NeedsAddPath(Param: string): boolean;
var
  OrigPath: string;
begin
  if not RegQueryStringValue(HKEY_LOCAL_MACHINE, ENVIRONMENT_KEY, 'Path', OrigPath)
  then begin
    Result := True;
    exit;
  end;
  { look for the path with leading and trailing semicolon }
  { Pos() returns 0 if not found }
  Result := Pos(';' + Param + ';', ';' + OrigPath + ';') = 0;
end;

procedure AddPath(Param: string);
var OrigPath: string;
begin
  Log('Adding path: ' + Param);
  RegQueryStringValue(HKEY_LOCAL_MACHINE, ENVIRONMENT_KEY, 'Path', OrigPath);
  RegWriteStringValue(HKEY_LOCAL_MACHINE, ENVIRONMENT_KEY, 'Path', OrigPath + ';' + Param);
end;

procedure CurStepChanged(CurStep: TSetupStep);
var 
  BinPath: String;
begin
  if CurStep = ssPostInstall then begin
    BinPath := 'C:\bin';
    if NeedsAddPath(BinPath) then begin
      AddPath(BinPath);
    end;
  end;
end;
