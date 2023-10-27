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
set subfolderSelection=text

:: Load cmd vars from json including:
:: - %robotsBaseFolder%
:: - %activeRobot%
:: - %roboIP%
:: - %normalizeSource%
CALL %~dp0\___loadActiveRobot.bat "___subfolderSelection=%subfolderSelection%"
CALL %~dp0\__getActiveRobotVars.bat

:: Sub folder with source files
set _sourceDirectory=%robotsBaseFolder%\%activeRobot%\source

:: set subfolder to binary for output files, refresh variables
set subfolderSelection=binary
CALL %~dp0\___loadActiveRobot.bat "___subfolderSelection=%subfolderSelection%"
CALL %~dp0\__getActiveRobotVars.bat
:: Sub folder to save .tp files
set _outputDirectory=%robotsBaseFolder%\%activeRobot%\bin

:: Create Subfolders
setlocal enableextensions
mkdir %_outputDirectory%
endlocal

for %%f in (%_sourceDirectory%\*.LS) do %~dp0\lib\maketp.exe %%f %_outputDirectory%\%%~nf.TP

if [%1]== PAUSED (pause)
if [%1]== STOP (cmd /k)
if [%1]== CONT (exit /B)
if [%1]==[] (cmd /k)
