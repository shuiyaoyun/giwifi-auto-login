Set WshShell = CreateObject("WScript.Shell")
userProfile = WshShell.ExpandEnvironmentStrings("%USERPROFILE%")
pythonPath = "D:\Anaconda3\pythonw.exe"
scriptPath = userProfile & "\auto_login.py"
WshShell.Run pythonPath & " " & chr(34) & scriptPath & chr(34), 0, False
