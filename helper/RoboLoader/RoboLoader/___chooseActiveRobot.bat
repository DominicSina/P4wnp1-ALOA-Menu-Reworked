@echo off

:: Load cmd vars from json including:
:: - %robotsBaseFolder%
:: - %activeRobot%
:: - %roboIP%
CALL %~dp0\___loadActiveRobot.bat
CALL %~dp0\__getActiveRobotVars.bat
@echo off

set oldRobot=%activeRobot%

:: Prompt user input if necessary
set newRobot=%1
if [%1]==[] (set /p newRobot="Enter activeRobot: ")

:: Replace old activeRobot with new one
SETLOCAL ENABLEDELAYEDEXPANSION
@for /f "delims=" %%a in (%~dp0\robotEnv.json) do (
    SET s=%%a
    SET s=!s:"activeRobot": "%oldRobot%"="activeRobot": "%newRobot%"!
    echo !s!>>%~dp0\tmpEnv.json
)

:: Overwrite old file
move %~dp0\tmpEnv.json %~dp0\robotEnv.json >nul

echo SET ROBOT FINISHED
echo ACTIVE ROBOT IS: %newRobot%
