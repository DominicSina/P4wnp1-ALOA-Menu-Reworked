@echo off
set %1 ::__roboIP
set %2 ::__roboPort
set %3 ::__ftpScript
set %4 ::__ftpCommandsFile


:: Prepare FTP commands
cd %~dp0
echo open ftp://user@%__roboIP%:%__roboPort%>%__ftpScript%
echo option batch on>>%__ftpScript%
echo option confirm off>>%__ftpScript%
echo.>>%__ftpScript%
echo.>>%__ftpScript%
copy "%__ftpScript%" + "%__ftpCommandsFile%" "%__ftpScript%"
echo.>>%__ftpScript%
echo exit>>%__ftpScript%
