' ============================================================
'   MAX — Auto-Start Script for Windows
'   Place this file (or a shortcut) in your Startup folder:
'     Win+R → shell:startup → paste this file
'
'   This launches MAX with GUI on Windows login.
' ============================================================

Dim WshShell
Set WshShell = CreateObject("WScript.Shell")

' Path to your MAX project
Dim projectPath
projectPath = "c:\Users\piyus\Downloads\jarvis_mvp\MAX"

' Full path to Python (pythonw = no console window)
Dim pythonPath
pythonPath = "C:\Python313\pythonw.exe"

' Launch MAX
WshShell.CurrentDirectory = projectPath
WshShell.Run """" & pythonPath & """ run.py", 0, False

Set WshShell = Nothing
