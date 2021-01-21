unit uBuildCommandEditor;

interface

{$I DelphiDefines.Inc}

uses Windows, SysUtils, Classes, Graphics, Forms, Controls, StdCtrls, Buttons, ExtCtrls, Grids, ComCtrls, uBuildMisc, Menus;

type
  TBuildCommandEditorDlg = class(TForm)
    ButtonOK: TButton;
    ButtonCancel: TButton;
    ButtonInsert: TButton;
    PanelBase: TPanel;
    Editor: TMemo;
    Splitter1: TSplitter;
    MacroValues: TListView;
    ButtonToggle: TButton;
    pmMacro: TPopupMenu;
    mniAddMacro: TMenuItem;
    mniDeleteMacro: TMenuItem;
    mniEditMacro: TMenuItem;
    procedure ButtonInsertClick(Sender: TObject);
    procedure ButtonToggleClick(Sender: TObject);
    procedure mniAddMacroClick(Sender: TObject);
    procedure mniEditMacroClick(Sender: TObject);
    procedure mniDeleteMacroClick(Sender: TObject);
    procedure pmMacroPopup(Sender: TObject);
  private
    { Private declarations }
    procedure SetButtons;
  public
    { Public declarations }
    procedure ToggleMacroDisplay();
    procedure PopulateDefaultMacros();
  end;

  function ShowBuildCommandEditor(ACaption: String; ACommandStr: String): String;

implementation

{$R *.dfm}

uses  uBuildEngine, uBuildMacroEditor;

function ShowBuildCommandEditor(ACaption: String; ACommandStr: String): String;
var
  dlg: TBuildCommandEditorDlg;
begin
   dlg := TBuildCommandEditorDlg.Create(Application);
   try
     dlg.PopulateDefaultMacros;
     dlg.Editor.Text := ACommandStr;
     dlg.Caption := Format('%s-build Event Command Line', [ACaption]);
     if (mrOK = dlg.ShowModal) then
       Result := dlg.Editor.Text
     else
       Result := ACommandStr;
   finally
     dlg.Free;
   end;
end;

procedure TBuildCommandEditorDlg.ButtonInsertClick(Sender: TObject);
begin
  if Assigned(MacroValues.Selected) then
    Editor.SelText := Format('$(%s)', [MacroValues.Selected.Caption]);
end;

procedure TBuildCommandEditorDlg.ToggleMacroDisplay;
begin
  if (MacroValues.Visible) then
  begin
    Splitter1.Visible := False;
    MacroValues.Visible := False;
    Height := 310;
    ButtonToggle.Caption := 'Macros >>';
  end else
  begin
    Splitter1.Visible := True;
    MacroValues.Visible := True;
    Height := 500;
    ButtonToggle.Caption := '<< Macros';
  end;
end;

procedure TBuildCommandEditorDlg.ButtonToggleClick(Sender: TObject);
begin
  ToggleMacroDisplay();
end;

procedure TBuildCommandEditorDlg.PopulateDefaultMacros;
var
  I: Integer;
begin
  try
    if Assigned(BuildEngine) then
    begin
      for I:= 0 to BuildEngine.MacroList.Count -1 do
        with MacroValues.Items.Add do
        begin
          Caption := BuildEngine.MacroList.Names[I];
          {$IFDEF D6_UP}
          SubItems.Add(BuildEngine.MacroList.ValueFromIndex[I]);
          {$ELSE}
          SubItems.Add(BuildEngine.MacroList.Values[BuildEngine.MacroList.Names[I]]);
          {$ENDIF}
        end;
    end;

    SetButtons();
  except
    ButtonInsert.Visible := False;
  end;
end;

procedure TBuildCommandEditorDlg.SetButtons();
begin
  ButtonInsert.Enabled := (MacroValues.Items.Count > 0);
  mniEditMacro.Enabled := (MacroValues.SelCount > 0);
  mniDeleteMacro.Enabled := (MacroValues.SelCount > 0);
end;

procedure TBuildCommandEditorDlg.mniAddMacroClick(Sender: TObject);
var
  sName, sPath: String;
begin
  if (EditMacroItem('Add', sName, sPath)) then
  begin
    with MacroValues.Items.Add do
    begin
      Caption := sName;
      SubItems.Add(sPath);
    end;
    BuildEngine.AddMacro(sName, sPath);
  end;
end;

procedure TBuildCommandEditorDlg.mniEditMacroClick(Sender: TObject);
var
  sOldName, sName, sPath: String;
begin
  if (MacroValues.Selected = nil) then Exit;

  sName := MacroValues.Selected.Caption;
  sOldName:= sName;
  sPath := MacroValues.Selected.SubItems.Strings[0];
  if (EditMacroItem('Edit', sName, sPath)) then
  begin
    with MacroValues.Selected do
    begin
      Caption := sName;
      SubItems.Strings[0] := sPath;
    end;
    BuildEngine.EditMacro(sOldName, sName, sPath);
  end;
end;

procedure TBuildCommandEditorDlg.mniDeleteMacroClick(Sender: TObject);
var
  sName: String;
begin
  if (MacroValues.Selected = nil) then Exit;
  sName := MacroValues.Selected.Caption;
  MacroValues.Selected.Delete;
  BuildEngine.DeleteMacro(sName);
end;

procedure TBuildCommandEditorDlg.pmMacroPopup(Sender: TObject);
begin
  SetButtons;
end;

end.
