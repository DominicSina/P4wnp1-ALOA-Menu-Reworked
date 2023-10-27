@echo off
set %1 ::__localFtpDirectory
set %2 ::__ftpScript


:: Create Subfolders
setlocal enableextensions
mkdir %__localFtpDirectory%
endlocal
:: Navigate Subfolders
cd /d %__localFtpDirectory%

:: Run FTP commands
"%~dp0\lib\WinSCP\winscp.com" /script="%__ftpScript%"
IF /I "%ERRORLEVEL%" EQU "0" (
    ECHO FILE TRANSFER SUCCESSFUL
) ELSE (
    ECHO ERROR DURING FILE TRANSFER
)
