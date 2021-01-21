unit uExpressionBreakpoint;

interface

uses
  Classes, SysUtils, ToolsAPI;


{
Reference: http://www.gexperts.org/open-tools-api-faq/#editorcontext

How can I add menu items to the code editor’s popup menu?
IOTAEditView.GetEditWindow.Form.FindComponent(‘EditorLocalMenu’) will return the editor’s TPopupMenu component that you can add to.
Your added menu items will work best if you add them to the end of the popup menu and may not work at all if you associate an action with them.
Note that you might want an IOTAEditorNotifier to determine when to add your new menu items to new editor windows.
}

type
  TSourceEditorNotifier = class(TNotifierObject, IOTANotifier, IOTAEditorNotifier)
  private
    FEditor: IOTASourceEditor;
    FIndex: Integer;

    { IOTANotifier }
    procedure Destroyed;

    { IOTAEditorNotifier }
    procedure ViewActivated(const View: IOTAEditView);
    procedure ViewNotification(const View: IOTAEditView; Operation: TOperation);

    procedure ExpressionMenuItemClick(Sender: TObject);
    procedure CloseAllButThisMenuItemClick(Sender: TObject);
  public
    constructor Create(AEditor: IOTASourceEditor);
    destructor Destroy; override;
  end;

  TIDENotifier = class(TNotifierObject, IOTANotifier, IOTAIDENotifier)
  private
    { IOTAIDENotifier }
    procedure FileNotification(NotifyCode: TOTAFileNotification; const FileName: string; var Cancel: Boolean);
    procedure BeforeCompile(const Project: IOTAProject; var Cancel: Boolean); overload;
    procedure AfterCompile(Succeeded: Boolean); overload;
  end;

procedure Register;

implementation

uses
  Windows, Messages, Menus, Forms, ActnList;

var
  SourceEditorNotifiers: TList = nil;
  IDENotifierIndex: Integer = -1;
  ExpressionMenuItem: TMenuItem = nil;
  CloseAllButThisMenuItem: TMenuItem = nil;
//----------------------------------------------------------------------------------------------------------------------

procedure ClearSourceEditorNotifiers;
var
  I: Integer;
begin
  if Assigned(SourceEditorNotifiers) then
    for I := SourceEditorNotifiers.Count - 1 downto 0 do
      // Destroyed calls RemoveNotifier which in turn releases the instance
      TSourceEditorNotifier(SourceEditorNotifiers[I]).Destroyed;
end;

//----------------------------------------------------------------------------------------------------------------------

procedure InstallSourceEditorNotifiers(Module: IOTAModule);
var
  I: Integer;
  SourceEditor: IOTASourceEditor;
begin
  for I := 0 to Module.ModuleFileCount - 1 do
    if Supports(Module.ModuleFileEditors[I], IOTASourceEditor, SourceEditor) then
    begin
      SourceEditorNotifiers.Add(TSourceEditorNotifier.Create(SourceEditor));
      SourceEditor := nil;
    end;
end;

procedure Register;
var
  Services: IOTAServices;
  ModuleServices: IOTAModuleServices;
  EditorServices: IOTAEditorServices;
  EditorTopView: IOTAEditView;
  I, J: Integer;
begin
  SourceEditorNotifiers := TList.Create;
  // install IDE notifier so that we can install editor notifiers for any newly opened module
  Services := BorlandIDEServices as IOTAServices;
  IDENotifierIndex := Services.AddNotifier(TIDENotifier.Create);

  // install editor notifiers for all currently open modules
  ModuleServices := (BorlandIDEServices as IOTAModuleServices);
  if ModuleServices.ModuleCount = 0 then Exit;
  for I := 0 to ModuleServices.ModuleCount - 1 do
    InstallSourceEditorNotifiers(ModuleServices.Modules[I]);

  // hook currently active module
  EditorServices := BorlandIDEServices as IOTAEditorServices;
  if not Assigned(EditorServices) then Exit;

  EditorTopView := EditorServices.TopView;
  if not Assigned(EditorTopView) then Exit;

  for I := 0 to SourceEditorNotifiers.Count - 1 do
    with TSourceEditorNotifier(SourceEditorNotifiers[I]) do
      for J := 0 to FEditor.EditViewCount - 1 do
        if FEditor.EditViews[J] = EditorTopView then
        begin
          ViewActivated(EditorTopView);
          Exit;
        end;
end;

procedure RemoveIDENotifier;
var
  Services: IOTAServices;
begin
  Services := BorlandIDEServices as IOTAServices;
  if Assigned(Services) then
    Services.RemoveNotifier(IDENotifierIndex);
end;

type
  TWatchMenuItem = class(TMenuItem)
  public
    destructor Destroy; override;
  end;


{ TWatchMenuItem public }

// Editor notifiers are not fired when Delphi is terminating; in that case the menu item will be freed by the parent
// menu; we need to nil the global var MenuItem so that finalization does not attempt to destroy an invalid pointer

destructor TWatchMenuItem.Destroy;
begin
  ExpressionMenuItem := nil;
  CloseAllButThisMenuItem := nil;
  
  inherited Destroy;
end;

{ TSourceEditorNotifier private: IOTANotifier }

procedure TSourceEditorNotifier.Destroyed;
begin
  FEditor.RemoveNotifier(FIndex);
end;

{ TSourceEditorNotifier private: IOTAEditorNotifier }

procedure TSourceEditorNotifier.ViewActivated(const View: IOTAEditView);
var
  EditWindow: INTAEditWindow;
  EditWindowForm: TCustomForm;
  EditorLocalMenu: TComponent;
  ParentMenu: TMenu;
begin
  EditWindow := View.GetEditWindow;
  if not Assigned(EditWindow) then Exit;

  EditWindowForm := EditWindow.Form;
  if not Assigned(EditWindowForm) then Exit;

  EditorLocalMenu := EditWindowForm.FindComponent('EditorLocalMenu');
  if not Assigned(EditorLocalMenu) then Exit;

  if not Assigned(ExpressionMenuItem) then
    ExpressionMenuItem := TWatchMenuItem.Create(nil);
  try
    if (EditorLocalMenu is TMenu) then
    begin
      ParentMenu := ExpressionMenuItem.GetParentMenu;
      if Assigned(ParentMenu) then
        ParentMenu.Items.Remove(ExpressionMenuItem);

      TMenu(EditorLocalMenu).Items.Add(ExpressionMenuItem);
      ExpressionMenuItem.Caption := 'Add Expression Breakpoint';
      ExpressionMenuItem.OnClick := ExpressionMenuItemClick;
    end;
  except
    FreeAndNil(ExpressionMenuItem);
    raise;
  end;
  {
  if not Assigned(CloseAllButThisMenuItem) then
    CloseAllButThisMenuItem := TWatchMenuItem.Create(nil);
  try
    if (EditorLocalMenu is TMenu) then
    begin
      ParentMenu := CloseAllButThisMenuItem.GetParentMenu;
      if Assigned(ParentMenu) then
        ParentMenu.Items.Remove(CloseAllButThisMenuItem);

      TMenu(EditorLocalMenu).Items.Add(CloseAllButThisMenuItem);
      CloseAllButThisMenuItem.Caption := 'Close All but This';
      CloseAllButThisMenuItem.OnClick := CloseAllButThisMenuItemClick;
    end;
  except
    FreeAndNil(CloseAllButThisMenuItem);
    raise;
  end;
   }
end;

procedure TSourceEditorNotifier.ViewNotification(const View: IOTAEditView; Operation: TOperation);
begin
  if Operation = opRemove then
  begin
    FreeAndNil(ExpressionMenuItem);
    FreeAndNil(CloseAllButThisMenuItem);
  end;
end;

{ TSourceEditorNotifier private }
procedure TSourceEditorNotifier.ExpressionMenuItemClick(Sender: TObject);
var
  EditorServices: IOTAEditorServices;
  EditorTopView: IOTAEditView;
  CheckView: IOTAEditView;
  DataEditorActions: TComponent;
  ActionToggleBreakpoint: TAction;
  DebuggerServices: IOTADebuggerServices;
  I: Integer;
  Breakpoint: IOTABreakpoint;
begin
  EditorServices := BorlandIDEServices as IOTAEditorServices;
  EditorTopView := EditorServices.TopView;

  if not Assigned(EditorTopView) then Exit; // should never happen
  if FEditor.EditViewCount = 0 then  Exit;  // should never happen

  // check the top view; it should be one of this source editor's views
  CheckView := nil;
  for I := 0 to FEditor.EditViewCount - 1 do
    if (FEditor.EditViews[I] = EditorTopView) or (FEditor.EditViews[I].SameView(EditorTopView)) then
    begin
      CheckView := FEditor.EditViews[I];
      Break;
    end;

  if not Assigned(CheckView) then  Exit;
  if not Assigned(CheckView.Block) or (CheckView.Block.Text = '') then Exit; // no text selected; nothing to do

  // find 'Toggle Breakpoint' action
  DataEditorActions := Application.FindComponent('EditorActionLists');
  if not Assigned(DataEditorActions) then Exit;
  ActionToggleBreakpoint := DataEditorActions.FindComponent('ecToggleBreakpoint') as TAction;
  if not Assigned(ActionToggleBreakpoint) then Exit;

  DebuggerServices := BorlandIDEServices as IOTADebuggerServices;
  with DebuggerServices do
  begin
    // toggle breakpoint
    if not ActionToggleBreakpoint.Execute then Exit;
    // attempt to find the added breakpoint
    Breakpoint := nil;
    for I := 0 to SourceBkptCount - 1 do
      with SourceBkpts[I] do
        if (FileName = FEditor.FileName) and (LineNumber = CheckView.Block.StartingRow) then
        begin
          Breakpoint := SourceBkpts[I];
          Break;
        end;

    // if not found then we have just toggled off an existing breakpoint
    if not Assigned(Breakpoint) then
    begin
      // toggle again to add a new one
      if not ActionToggleBreakpoint.Execute then Exit;
      // attempt to find the added breakpoint
      Breakpoint := nil;
      for I := 0 to SourceBkptCount - 1 do
        with SourceBkpts[I] do
          if (FileName = FEditor.FileName) and (LineNumber = CheckView.Block.StartingRow) then
          begin
            Breakpoint := SourceBkpts[I];
            Break;
          end;
    end;

    // set breakpoint properties
    if not Assigned(Breakpoint) then Exit;

    with Breakpoint do
    begin
      DoBreak := False;
      LogMessage := '';
      EvalExpression := CheckView.Block.Text;
      LogResult := True;
    end;
  end;
end;

procedure TSourceEditorNotifier.CloseAllButThisMenuItemClick(Sender: TObject);
var
  EditorServices: IOTAEditorServices;
  EditorTopView: IOTAEditView;
  CheckView: IOTAEditView;
  EditActions: IOTAEditActions;
  I: Integer;
begin
  EditActions := BorlandIDEServices as IOTAEditActions;
  EditorServices := BorlandIDEServices as IOTAEditorServices;
  EditorTopView := EditorServices.TopView;

  if not Assigned(EditActions) then Exit;
  if not Assigned(EditorTopView) then Exit; // should never happen
  if FEditor.EditViewCount = 0 then  Exit;  // should never happen

  CheckView := EditorTopView;

  for I := FEditor.EditViewCount - 1 downto 0 do
  begin
    if (FEditor.EditViews[I] <> CheckView) or
       (not FEditor.EditViews[I].SameView(CheckView)) then
    begin
      EditActions.ClosePage;
    end;
  end;
end;

{ TSourceEditorNotifier public }
constructor TSourceEditorNotifier.Create(AEditor: IOTASourceEditor);
begin
  inherited Create;
  FEditor := AEditor;
  FIndex := FEditor.AddNotifier(Self);
end;

destructor TSourceEditorNotifier.Destroy;
begin
  SourceEditorNotifiers.Remove(Self);
  FEditor := nil;
  inherited Destroy;
end;

{ TIDENotifier private: IOTAIDENotifier }
procedure TIDENotifier.AfterCompile(Succeeded: Boolean);
begin
  // do nothing
end;

procedure TIDENotifier.BeforeCompile(const Project: IOTAProject; var Cancel: Boolean);
begin
  // do nothing
end;

procedure TIDENotifier.FileNotification(NotifyCode: TOTAFileNotification; const FileName: string; var Cancel: Boolean);
var
  ModuleServices: IOTAModuleServices;
  Module: IOTAModule;
begin
  case NotifyCode of
    ofnFileOpened:  begin
                      ModuleServices := BorlandIDEServices as IOTAModuleServices;
                      Module := ModuleServices.FindModule(FileName);
                      if Assigned(Module) then InstallSourceEditorNotifiers(Module);
                    end;
  end;
end;

initialization

finalization
  RemoveIDENotifier;
  ClearSourceEditorNotifiers;
  FreeAndNil(SourceEditorNotifiers);
  FreeAndNil(ExpressionMenuItem);
  FreeAndNil(CloseAllButThisMenuItem);

end.
