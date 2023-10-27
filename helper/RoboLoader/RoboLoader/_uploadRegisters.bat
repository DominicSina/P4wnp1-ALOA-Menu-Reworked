::######################################################
::# Type of backup, determines which files and subfolder
::# Currently supported:
::# - aoa (same as All of Above)
::# - all (complete Robot root dir)
::# - source (.LS files to all user defined .TP progs)
::# - bin (.TP files of all user defined .TP progs)
::#
::# To add type "xyz" create xyzTypeFileList.txt
::# with desired FTP commands. Then set backupType
::# to xyz.
::######################################################
set backupType=registers

:: Prompt user input if necessary
set confirmation=%2
if [%2]==[] (set /p confirmation="Are You Sure?[Y/N]: ")
if not %confirmation%== Y exit

::######################################################
::# Determines which folder %subfolder% points to. 
::# The different %subfolder% paths can be defined  in
::# robotEnv.json.
::# Currently supported:
::# - text   (textFolder from robotEnv will be used)
::# - binary (binaryFolder from robotEnv will be used)
::# - misc   (miscFolder from robotEnv will be used)
::#
::# In robotEnv.json %subfolder% can then be used e.g.
::# in robotsBaseFolder.
::######################################################
set subfolderSelection=binary

:: Load cmd vars from json including:
:: - %robotsBaseFolder%
:: - %activeRobot%
:: - %roboIP%
:: - %normalizeSource%
CALL %~dp0\___loadActiveRobot.bat "___subfolderSelection=%subfolderSelection%"
CALL %~dp0\__getActiveRobotVars.bat

:: Write "Upload" or "Download" depending on which commands should be run
set _ftpCommandsFile=%~dp0\FtpCommandFiles\%backupType%WinscpUploadCommands.txt

:: Those should not be changed
set _localFtpDirectory=%robotsBaseFolder%\%activeRobot%\aoa
set _ftpScript=%~dp0\winscpFtpScript.ftp

CALL %~dp0\__writeWinscpFtpScript.bat "__roboIP=%roboIP%" "__roboPort=%roboPort%" "__ftpScript=%_ftpScript%" "__ftpCommandsFile=%_ftpCommandsFile%"
CALL %~dp0\__executeWinscpFtpScript.bat "__localFtpDirectory=%_localFtpDirectory%" "__ftpScript=%_ftpScript%"
CALL %~dp0\__allFilesInFtpDirToUpperCase.bat "__localFtpDirectory=%_localFtpDirectory%"

ECHO SCRIPT FINISHED
if [%1]== PAUSED (pause)
if [%1]== STOP (cmd /k)
if [%1]== CONT (exit /B)
if [%1]==[] (cmd /k)
