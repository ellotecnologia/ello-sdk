{ ********************************************************************** }
{ ******** Custom Delphi IDE Build Notifier for Build Options ********** }
{ ******* Written by Kiran Kurapaty (kuraki@morganstanley.com) ********* }
{ ********************************************************************** }
unit uBuildNotifier;

interface

{$I DelphiDefines.inc}

uses
  Windows, SysUtils, Controls, Graphics, Classes, Menus, ActnList, ToolsAPI, Dialogs, Forms;

type
  TBuildNotifier = class(TNotifierObject, IOTAIDENotifier, IOTAIDENotifier50)
  private
  protected
    { This procedure is to load files related }
    procedure ListFiles(AList : TStrings; AFileName : String);
    { This procedure is to check if we are processing correct file for our purpose }
    function InValidExtension(AFileName : String): Boolean;
    function InValidExtensions(AFileName: String): Boolean;
  public

    procedure BeforeCompile(const Project: IOTAProject; var Cancel: Boolean); overload;
    { Same as BeforeCompile on IOTAIDENotifier except indicates if the compiler was invoked due to a CodeInsight compile }
    procedure BeforeCompile(const Project: IOTAProject; IsCodeInsight: Boolean; var Cancel: Boolean); overload;

    procedure AfterCompile(Succeeded: Boolean); overload;
    { Same as AfterCompile on IOTAIDENotifier except indicates if the compiler was invoked due to a CodeInsight compile }
    procedure AfterCompile(Succeeded: Boolean; IsCodeInsight: Boolean); overload;
    { This procedure is called for many various file operations within the IDE }
    procedure FileNotification(ANotifyCode: TOTAFileNotification; const AFileName: String; var ACancel: Boolean);
  end;

implementation

uses
  uBuildOptionExpert, uBuildMisc;


const
  C_OTA_FILE_NOTIFICATION_STR : array [TOTAFileNotification] of String = (
    'ofnFileOpening', 'ofnFileOpened', 'ofnFileClosing',
    'ofnDefaultDesktopLoad', 'ofnDefaultDesktopSave', 'ofnProjectDesktopLoad',
    'ofnProjectDesktopSave', 'ofnPackageInstalled', 'ofnPackageUninstalled'
    {$IFDEF D6_UP}, 'ofnActiveProjectChanged'{$ENDIF} );

{ TBuildNotifier }

procedure TBuildNotifier.AfterCompile(Succeeded: Boolean);
begin
 // Do nothing, keep it for backward compatibility
end;

procedure TBuildNotifier.AfterCompile(Succeeded: Boolean; IsCodeInsight: Boolean);
begin
  if (not IsCodeInsight) then
    BuildOptionExpert.TriggerPostBuildEvent(Succeeded);
end;

procedure TBuildNotifier.BeforeCompile(const Project: IOTAProject; var Cancel: Boolean);
begin
 // Do nothing, keep it for backward compatibility
end;

procedure TBuildNotifier.BeforeCompile(const Project: IOTAProject; IsCodeInsight: Boolean; var Cancel: Boolean);
begin
  if (not IsCodeInsight) then
    BuildOptionExpert.ExecutePreBuildEvent();
end;

procedure TBuildNotifier.FileNotification(ANotifyCode: TOTAFileNotification; const AFileName: String; var ACancel: Boolean);
begin
  if (not InValidExtensions(AFileName)) then Exit;
  LogText('TBuildNotifier.FileNotification (Code: %s, File: %s)', [C_OTA_FILE_NOTIFICATION_STR[ANotifyCode], AFileName]);
  case (ANotifyCode) of
    { the file passed in FileName is opening where FileName is the name of the file being opened }
    ofnFileOpening:           ; // do nothing
    { the file passed in FileName has opened where FileName is the name of the file that was opened }
    ofnFileOpened:            BuildOptionExpert.LoadBuildOptions(AFileName);
    { the file passed in FileName is closing where FileName is the name of the file being closed }
    ofnFileClosing:           BuildOptionExpert.Options.Reset();
    { I haven’t found when this is triggered in my test but I assume it is when the IDE loads the Default Desktop settings }
    ofnDefaultDesktopLoad:    ; // do nothing
    { I haven’t found when this is triggered in my test but I assume it is when the IDE saves the Default Desktop settings }
    ofnDefaultDesktopSave:    ; // do nothing
    { this is triggered when the IDE loads a project’s desktop settings where FileName is the name of the desktop settings file }
    ofnProjectDesktopLoad:    ; // BuildOptionExpert.LoadBuildOptions(AFileName);
    { this is triggered when the IDE saves a project’s desktop settings where FileName is the name of the desktop settings file }
    ofnProjectDesktopSave:    ; // do nothing
    { this is triggered when a package (BPL) list loaded by the IDE where FileName is the name of the BPL file }
    ofnPackageInstalled:      ; // do nothing
    { this is triggered when a package (BPL) list unloaded by the IDE where FileName is the name of the BPL file }
    ofnPackageUninstalled:    ; // do nothing
    { this is triggered when a project is made active in the IDE’s Project Manager where the FileName is the project file
      (.dproj, bdsproj or .dpr for older version of Delphi) }
    {$IFDEF D6_UP}
    ofnActiveProjectChanged:  ; // BuildOptionExpert.LoadBuildOptions(AFileName);
    {$ENDIF}
  end;
  LogText('TBuildNotifier.FileNotification (Code: %s, File: %s)', [C_OTA_FILE_NOTIFICATION_STR[ANotifyCode], AFileName]);
end;

function TBuildNotifier.InValidExtensions(AFileName: String): Boolean;
const
  VALID_EXT : Array[0..2] of String = ('.dpr', '.bpg', '.dpk' );
var
  sExt : String;
  I : Integer;
begin
  Result := False;

  sExt := Lowercase(ExtractFileExt(AFileName));
  for I:= Low(VALID_EXT) to High(VALID_EXT) do
    if sExt = VALID_EXT[I] then
    begin
      Result := True;
      Break;
    end;
end;

function TBuildNotifier.InValidExtension(AFileName: String): Boolean;
begin
  Result := ('.dpr' = LowerCase(ExtractFileExt(AFileName)));
end;

procedure TBuildNotifier.ListFiles(AList: TStrings; AFileName: String);
var
  sr  : TSearchRec;
begin
  AList.Clear;
  AFileName := ChangeFileExt(AFileName, '.*');

  if FindFirst(AFileName, faAnyFile, sr) = 0 then
  begin
    repeat
      if InValidExtensions(sr.Name) then
        AList.Add(ExtractFilePath(AFileName) + sr.Name);
    until FindNext(sr) <> 0;
    FindClose(sr);
  end;
end;

end.

