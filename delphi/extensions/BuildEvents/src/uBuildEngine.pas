unit uBuildEngine;

interface

{$I DelphiDefines.inc}

uses
  Windows, Messages, SysUtils, Classes, Forms, Dialogs;

type
  EPipeError        = class(Exception);
  EBuildEngineError = class(Exception);

  TBuildEngine = class(TObject)
  private
    FLastCmd,
    FLastOutput: String;
    FMacroList: TStringList;
    function GetMacroList: TStringList;
  protected
    function RunPipe(psCommandLine, psWorkDir : String; phInputHandle : THandle) : String; overload;
    function RunPipe(psCommandLine, psWorkDir : String) : String; overload;
    function OpenInputFile(AFileName : String) : THandle;
    procedure CloseInputFile(phHandle : THandle);
    function GetBuildMacroValue(AName: String): String;
    function ExpandBuildMacros(AParams: String): String;
  public
    constructor Create; virtual;
    destructor Destroy; override;

    function Command(const AParams: String) : String; overload;
    function Command(const AParams, ARunDir: String): String; overload;
    function Command(const AParams, ARunDir: String; AInputData : TStrings) : String; overload;
    function Command(const AParams, ARunDir: String; AInputData : String) : String; overload;

    procedure RefreshMacros;
    procedure AddMacro(AName, AValue: String);
    procedure EditMacro(AName, ANewName, AValue: String);
    procedure DeleteMacro(AName: String);

    property LastCmd : String read FLastCmd;
    property LastOutput : String read FLastOutput;
    property MacroList: TStringList read GetMacroList;
  end;

var
  BuildEngine : TBuildEngine;

implementation

uses
  uBuildMisc, {$IFDEF D6_UP}DateUtils, {$ENDIF} Registry, uBuildOptionExpert;

const
  BUFFER_SIZE = 4096;
  MAX_CMDLINE_SIZE = 1024;

{ TBuildEngine }
procedure TBuildEngine.CloseInputFile(phHandle: THandle);
begin
  CloseHandle(phHandle);
end;

constructor TBuildEngine.Create;
begin
  inherited Create;
  FLastCmd := '';
  FLastOutput := '';
end;

destructor TBuildEngine.Destroy;
begin
  if Assigned(FMacroList) then FMacroList.Free;

  inherited Destroy;
end;

function TBuildEngine.RunPipe(psCommandLine, psWorkDir: String; phInputHandle: THandle): String;
var
  iError, iBytesRead, hReadHandle,
  hWriteHandle  : Cardinal;
  Security      : TSecurityAttributes;
  ProcInfo      : TProcessInformation;
  Buf           : PByte;
  StartupInfo   : TStartupInfo;
  bDone         : Boolean;
  iCounter      : Integer;
  ACmdLine, AWorkDir: Array[0..MAX_CMDLINE_SIZE] of Char;
  sMesg, sComSpec: String;
begin
  Result := '';
  sComSpec := Trim({$IFDEF D6_UP} GetEnvironmentVariable {$ELSE} GetEnvVar {$ENDIF} ('COMSPEC'));
  Security.lpSecurityDescriptor := nil;
  Security.bInheritHandle := true;
  Security.nLength := SizeOf(Security);

  if CreatePipe(hReadHandle, hWriteHandle, @Security, BUFFER_SIZE) then
  begin
    try
      { Startup Info for command process }
      with StartupInfo do
      begin
        lpReserved := nil;
        lpDesktop := nil;
        lpTitle := nil;
        dwFlags := STARTF_USESTDHANDLES or STARTF_USESHOWWINDOW;
        cbReserved2 := 0;
        lpReserved2 := nil;
        { Prevent the command window being displayed }
        wShowWindow := SW_HIDE;
        { Standard Input - Default handle }
        if phInputHandle = 0 then
          hStdInput := GetStdHandle(STD_INPUT_HANDLE)
        else
          hStdInput := phInputHandle;
        { Standard Output - Point to Write end of pipe }
        hStdOutput := hWriteHandle;
        { Standard Error - Default handle }
        hStdError := GetStdHandle(STD_ERROR_HANDLE);
      end;

      StartupInfo.cb := SizeOf(StartupInfo);
      { Initialise CmdLine and WorkDir }
      FillChar(ACmdLine, MAX_CMDLINE_SIZE, #0);
      FillChar(AWorkDir, MAX_CMDLINE_SIZE, #0);

      { Create the command as a process }
      StrPCopy(ACmdLine, '/C '+ psCommandLine);
      StrPCopy(AWorkDir, psWorkDir);
      //BuildOptionExpert.LogLine(mtDebug, 'Executing: %s', [ACmdLine]);
      if CreateProcess(PAnsiChar(sComSpec), ACmdLine, nil, nil, True, CREATE_NEW_PROCESS_GROUP or NORMAL_PRIORITY_CLASS, nil, AWorkDir, StartupInfo, ProcInfo) then
      begin
        try
          { We don't need this handle any more, and keeping it open on this end
            will cause errors. It remains open for the child process though. }
          CloseHandle(hWriteHandle);
          { Allocate memory to the buffer }
          GetMem(Buf, BUFFER_SIZE * SizeOf(Char));
          try
            bDone := false;
            while not bDone do
            begin
              Application.ProcessMessages;
              if not Windows.ReadFile(hReadHandle, Buf^, BUFFER_SIZE, iBytesRead, nil) then
              begin
                iError := GetLastError;
                case iError of
                  ERROR_BROKEN_PIPE:
                        begin
                          // Broken pipe means client app has ended.
                          bDone := true;
                        end;
                  ERROR_INVALID_HANDLE: raise EPipeError.Create('Error: Invalid Handle');
                  ERROR_HANDLE_EOF:     raise EPipeError.Create('Error: End of file');
                  ERROR_IO_PENDING:  ; // Do nothing... just waiting
                  else  raise EPipeError.Create('Error: #' + IntToStr(iError));
                end;
              end;

              if iBytesRead > 0 then
              begin
                for iCounter := 0 to iBytesRead - 1 do
                  Result := Result + Char(PAnsiChar(Buf)[iCounter]);
              end;
            end;
          finally
            FreeMem(Buf, BUFFER_SIZE);
          end;
        finally
          CloseHandle(ProcInfo.hThread);
          CloseHandle(ProcInfo.hProcess);
        end
      end else
      begin
        sMesg := GetLastWindowsError;
        CloseHandle(hWriteHandle);
        raise EPipeError.CreateFmt('Error: %s.'#13#10'(Command="%s")', [sMesg, psCommandLine]);
      end;
    finally
      CloseHandle(hReadHandle);
    end;
  end;
end;

function TBuildEngine.OpenInputFile(AFileName: String): THandle;
var
  Security: TSecurityAttributes;
begin
  Security.lpSecurityDescriptor := nil;
  Security.bInheritHandle := true;
  Security.nLength := SizeOf(Security);

  Result := CreateFile(PChar(AFileName), GENERIC_READ, FILE_SHARE_READ, @Security, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, 0);
end;

function TBuildEngine.RunPipe(psCommandLine, psWorkDir: String): String;
begin
  Result := RunPipe(ExpandBuildMacros(psCommandLine), psWorkDir, 0);
end;

function TBuildEngine.Command(const AParams, ARunDir: String): String;
begin
  FLastCmd := ExpandBuildMacros(AParams);

  FLastOutput := RunPipe(FLastCmd, ARunDir);
  Result := FLastOutput;
end;

function TBuildEngine.Command(const AParams: String): String;
begin
  Result := Command(AParams, 'C:\');
end;

function TBuildEngine.Command(const AParams, ARunDir: String; AInputData: String): String;
var
  slInput : TStringList;
begin
  slInput := TStringList.Create;
  try
    slInput.Text := AInputData;
    Result := Command(AParams, ARunDir, slInput);
    //BuildOptionExpert.LogMessages(mtDebug, slInput);
  finally
    slInput.Free;
  end;
end;

function TBuildEngine.Command(const AParams, ARunDir: String; AInputData: TStrings): String;

  function GetTempFile: string;
  var
    PathName: array[0..MAX_PATH] of Char;
  begin
    Windows.GetTempPath(MAX_PATH, @PathName);
    Result := string(PathName);
    if AnsiLastChar(Result)^ <> '\' then Result := Result + '\';
    Result := Result + Format('build_output_%s.txt', [FormatDateTime('mmddyyy', Date)]);
  end;

var
  hInput : THandle;
begin
  FLastCmd := ExpandBuildMacros(AParams);

  Result := '';

  AInputData.SaveToFile(GetTempFile);
  try
    hInput := OpenInputFile(GetTempFile);
    try
      FLastOutput := RunPipe(FLastCmd, ARunDir, hInput);
      Result := FLastOutput;
    finally
      CloseInputFile(hInput);
    end;
  finally
    DeleteFile(GetTempFile);
  end;
end;

function TBuildEngine.GetMacroList: TStringList;
begin
  if not Assigned(FMacroList) or (FMacroList.Count = 0) then
    FMacroList := GetBuildMacroList;
  Result := FMacroList;
end;

function TBuildEngine.GetBuildMacroValue(AName: String): String;
begin
//  ProjectName, ProjectFileName, ProjectPath, ProjectExt, UnitOutputDir
//  TargetName, TargetFileName, TargetPath, TargetExt
//  WinDir, SysDir, TPlusClient, TPlusServer
  Result := '';
  if Assigned(MacroList) then
  begin
    Result := MacroList.Values[AName];
  end;
end;

function TBuildEngine.ExpandBuildMacros(AParams: String): String;
var
  I: Integer;
  sName, sValue: String;
begin
  Result := AParams;

  if Assigned(MacroList) then
  begin
    for I:= 0 to MacroList.Count -1 do
    begin
      sName := MacroList.Names[I];
      {$IFDEF D6_UP}
      sValue := MacroList.ValueFromIndex[I];
      {$ELSE}
      sValue := MacroList.Values[sName];
      {$ENDIF}
      Result := StringReplace(Result, Format('$(%s)', [sName]), sValue, [rfReplaceAll]);
    end;
  end;
end;

procedure TBuildEngine.RefreshMacros;
begin
  if Assigned(FMacroList) then
    FMacroList.Clear;
  FMacroList := GetBuildMacroList;
end;

procedure TBuildEngine.AddMacro(AName, AValue: String);
begin
  MacroList.Add(Format('%s=%s', [AName, AValue]));
  AddCustomMacro(AName, AValue);
end;

procedure TBuildEngine.DeleteMacro(AName: String);
var
  I: Integer;
begin
  I := MacroList.IndexOfName(AName);
  if (-1 <> I) then
    MacroList.Delete(I);

  DeleteCustomMacro(AName);
end;

procedure TBuildEngine.EditMacro(AName, ANewName, AValue: String);
var
  I: Integer;
begin
  I := MacroList.IndexOfName(AName);
  if (-1 <> I) then
    MacroList[I] := Format('%s=%s', [ANewName, AValue])
  else
    MacroList.Add(Format('%s=%s', [ANewName, AValue]));

  { Update Registry item }
  EditCustomMacro(AName, ANewName, AValue);
end;

initialization
  BuildEngine := TBuildEngine.Create;

finalization
  FreeAndNil(BuildEngine);

end.

