Set WshShell = CreateObject("WScript.Shell")
userProfile = WshShell.ExpandEnvironmentStrings("%USERPROFILE%")
cmd = "pythonw.exe """ & userProfile & "\auto_login.py"""
WshShell.Run cmd, 0, False
