; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Sounder3"
#define MyAppVersion "3.0"
#define MyAppPublisher "Mateusz Perczak"
#define MyAppURL "https://github.com/losek1/Sounder3"
#define MyAppExeName "Sounder3.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{4AD217F8-7375-4268-B5B3-EBF23E684930}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName}{#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName=C:\{#MyAppName}
DisableDirPage=no
DisableProgramGroupPage=yes
OutputDir=C:\Users\Mateusz\Desktop
OutputBaseFilename=Sounder3
SetupIconFile=C:\Users\Mateusz\Desktop\Sounder3\icon.ico
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\Mateusz\Desktop\Sounder3\Sounder3.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\_bz2.pyd"; DestDir: "{app}"; Flags: ignoreversion
;Source: "C:\Users\Mateusz\Desktop\Sounder3\_cffi_backend.cp36-win_amd64.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\_ctypes.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\_decimal.pyd"; DestDir: "{app}"; Flags: ignoreversion
;Source: "C:\Users\Mateusz\Desktop\Sounder3\_distutils_findvs.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\_hashlib.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\_lzma.pyd"; DestDir: "{app}"; Flags: ignoreversion
;Source: "C:\Users\Mateusz\Desktop\Sounder3\_multiprocessing.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\_socket.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\_ssl.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\_tkinter.pyd"; DestDir: "{app}"; Flags: ignoreversion
;Source: "C:\Users\Mateusz\Desktop\Sounder3\_win32sysloader.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\back_dark.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\back_light.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\base_library.zip"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\cover_art_dark.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\cover_art_light.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\error_light.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\errors.log"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\changelog.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\cfg.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\file_directory_dark.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\file_directory_light.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\forward_dark.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\forward_light.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\icon.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\libfreetype-6.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\libjpeg-8.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\libmpg123-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\libogg-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\libpng16-16.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\libtiff-5.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\libvorbis-0.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\libvorbisfile-3.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\libwebp-5.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\logo_1.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\_elementtree.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\pause_dark.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\pause_light.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\play_dark.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\play_light.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\previous_dark.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\previous_light.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\pyexpat.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\python36.dll"; DestDir: "{app}"; Flags: ignoreversion
;Source: "C:\Users\Mateusz\Desktop\Sounder3\pythoncom36.dll"; DestDir: "{app}"; Flags: ignoreversion
;Source: "C:\Users\Mateusz\Desktop\Sounder3\pywintypes36.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\refresh_dark.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\refresh_light.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\repeat_all_dark.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\repeat_all_light.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\repeat_none_dark.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\repeat_none_light.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\repeat_one_dark.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\repeat_one_light.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\SDL.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\SDL_image.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\SDL_mixer.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\SDL_ttf.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\select.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\settings_dark.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\settings_light.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\Sounder3.exe.manifest"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\tcl86t.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\tk86t.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\toggle_off_dark.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\toggle_off_light.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\toggle_on_dark.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\toggle_on_light.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\unicodedata.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\VCRUNTIME140.dll"; DestDir: "{app}"; Flags: ignoreversion
;Source: "C:\Users\Mateusz\Desktop\Sounder3\win32api.pyd"; DestDir: "{app}"; Flags: ignoreversion
;Source: "C:\Users\Mateusz\Desktop\Sounder3\win32trace.pyd"; DestDir: "{app}"; Flags: ignoreversion
;Source: "C:\Users\Mateusz\Desktop\Sounder3\win32ui.pyd"; DestDir: "{app}"; Flags: ignoreversion
;Source: "C:\Users\Mateusz\Desktop\Sounder3\win32wnet.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Mateusz\Desktop\Sounder3\zlib1.dll"; DestDir: "{app}"; Flags: ignoreversion
; Folders
Source: "C:\Users\Mateusz\Desktop\Sounder3\Include\*"; DestDir: "{app}\Include"; Flags: ignoreversion recursesubdirs createallsubdirs
;Source: "C:\Users\Mateusz\Desktop\Sounder3\lib2to3\*"; DestDir: "{app}\lib2to3\"; Flags: ignoreversion recursesubdirs createallsubdirs
;Source: "C:\Users\Mateusz\Desktop\Sounder3\lib2to3\tests\data\*"; DestDir: "{app}\lib2to3\tests\data\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Mateusz\Desktop\Sounder3\PIL\*"; DestDir: "{app}\PIL\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Mateusz\Desktop\Sounder3\pygame\*"; DestDir: "{app}\pygame\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Mateusz\Desktop\Sounder3\tcl\*"; DestDir: "{app}\tcl\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Mateusz\Desktop\Sounder3\tcl\encoding\*"; DestDir: "{app}\tcl\encoding\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Mateusz\Desktop\Sounder3\tcl\http1.0\*"; DestDir: "{app}\tcl\http1.0\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Mateusz\Desktop\Sounder3\tcl\msgs\*"; DestDir: "{app}\tcl\msgs\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Mateusz\Desktop\Sounder3\tcl\opt0.4\*"; DestDir: "{app}\tcl\opt0.4\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Mateusz\Desktop\Sounder3\tcl\tzdata\*"; DestDir: "{app}\tcl\tzdata\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Mateusz\Desktop\Sounder3\tcl\tzdata\Africa\*"; DestDir: "{app}\tcl\tzdata\Africa\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Mateusz\Desktop\Sounder3\tcl\tzdata\America\*"; DestDir: "{app}\tcl\tzdata\America\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Mateusz\Desktop\Sounder3\tcl\tzdata\America\Argentina\*"; DestDir: "{app}\tcl\tzdata\America\Argentina\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Mateusz\Desktop\Sounder3\tcl\tzdata\America\Indiana\*"; DestDir: "{app}\tcl\tzdata\America\Indiana\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Mateusz\Desktop\Sounder3\tcl\tzdata\America\Kentucky\*"; DestDir: "{app}\tcl\tzdata\America\Kentucky\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Mateusz\Desktop\Sounder3\tcl\tzdata\America\North_Dakota\*"; DestDir: "{app}\tcl\tzdata\America\North_Dakota\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Mateusz\Desktop\Sounder3\tcl\tzdata\Antarctica\*"; DestDir: "{app}\tcl\tzdata\Antarctica\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Mateusz\Desktop\Sounder3\tcl\tzdata\Arctic\*"; DestDir: "{app}\tcl\tzdata\Arctic\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Mateusz\Desktop\Sounder3\tcl\tzdata\Asia\*"; DestDir: "{app}\tcl\tzdata\Asia\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Mateusz\Desktop\Sounder3\tcl\tzdata\Atlantic\*"; DestDir: "{app}\tcl\tzdata\Atlantic\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Mateusz\Desktop\Sounder3\tcl\tzdata\Australia\*"; DestDir: "{app}\tcl\tzdata\Australia\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Mateusz\Desktop\Sounder3\tcl\tzdata\Brazil\*"; DestDir: "{app}\tcl\tzdata\Brazil\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Mateusz\Desktop\Sounder3\tcl\tzdata\Canada\*"; DestDir: "{app}\tcl\tzdata\Canada\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Mateusz\Desktop\Sounder3\tcl\tzdata\Chile\*"; DestDir: "{app}\tcl\tzdata\Chile\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Mateusz\Desktop\Sounder3\tcl\tzdata\Etc\*"; DestDir: "{app}\tcl\tzdata\Etc\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Mateusz\Desktop\Sounder3\tcl\tzdata\Europe\*"; DestDir: "{app}\tcl\tzdata\Europe\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Mateusz\Desktop\Sounder3\tcl\tzdata\Indian\*"; DestDir: "{app}\tcl\tzdata\Indian\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Mateusz\Desktop\Sounder3\tcl\tzdata\Mexico\*"; DestDir: "{app}\tcl\tzdata\Mexico\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Mateusz\Desktop\Sounder3\tcl\tzdata\Pacific\*"; DestDir: "{app}\tcl\tzdata\Pacific\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Mateusz\Desktop\Sounder3\tcl\tzdata\SystemV\*"; DestDir: "{app}\tcl\tzdata\SystemV\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Mateusz\Desktop\Sounder3\tcl\tzdata\US\*"; DestDir: "{app}\tcl\tzdata\US\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Mateusz\Desktop\Sounder3\tk\*"; DestDir: "{app}\tk\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Mateusz\Desktop\Sounder3\tk\images\*"; DestDir: "{app}\tk\images\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Mateusz\Desktop\Sounder3\tk\msgs\*"; DestDir: "{app}\tk\msgs\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Mateusz\Desktop\Sounder3\tk\ttk\*"; DestDir: "{app}\tk\ttk\"; Flags: ignoreversion recursesubdirs createallsubdirs
;Source: "C:\Users\Mateusz\Desktop\Sounder3\win32com\shell\*"; DestDir: "{app}\win32com\shell\"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files


[Icons]
Name: "{commonprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

