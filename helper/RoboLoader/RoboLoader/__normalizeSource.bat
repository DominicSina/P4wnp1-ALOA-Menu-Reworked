::######################################################
::# Normalizes content of source folder.
::# Only alters files with .ls / .LS extension.
::######################################################

@echo off
set %1 ::__localFtpDirectory

echo.
echo START NORMALIZING SOURCE

:: Create Subfolders
setlocal enableextensions
if not exist "%__localFtpDirectory%\headers" mkdir "%__localFtpDirectory%\headers"
if not exist "%__localFtpDirectory%\footers" mkdir "%__localFtpDirectory%\footers"
endlocal

setlocal enableDelayedExpansion
pushd "%__localFtpDirectory%"

:: put everything between(excluding) "/ATTR" and ending with "/MN" into .HEADER file
echo Extracting headers
for /r %%f in (*.ls) do CALL "%~dp0\lib\JREPL\JREPL.BAT" "(\/ATTR\r\n)([\s\S]*)(\/MN\r\n)" "" /MATCH /B /M /F %%f /O %__localFtpDirectory%\headers\%%~nf.HEADER

:: remove everything between(excluding) "/ATTR" and ending with "/MN"
echo Removing old headers
for /r %%i in (*.ls) do (CALL "%~dp0\lib\JREPL\JREPL.BAT" "(\/ATTR\r\n)([\s\S]*)(\/MN\r\n)" "$1$3" /B /M /F %%i /O %__localFtpDirectory%\%%~ni.tmp1 && move /Y "%%~ni.tmp1" "%%~i" >nul || echo -Error moving %%~ni.tmp1 to %%~ni.LS)


echo Removing linenumbers
:: remove line numbers
for /r %%i in (*.ls) do (CALL "%~dp0\lib\JREPL\JREPL.BAT" "\s*[0-9]*:" "    :" /B /INC "'/PROG'b:'/POS'be" /F %%i /O %__localFtpDirectory%\%%~ni.tmp2 && move /Y "%%~ni.tmp2" "%%~i" >nul || echo -Error moving %%~ni.tmp2 to %%~ni.LS)


:: put everything between "/POS"(including) and ending with "/END"(excluding) into .FOOTER file
echo Extracting footers
for /r %%f in (*.ls) do CALL "%~dp0\lib\JREPL\JREPL.BAT" "(\/POS\r\n)([\s\S]*)(\/END\r\n)" "" /MATCH /B /M /F %%f /O %__localFtpDirectory%\footers\%%~nf.FOOTER

:: remove everything between "/POS"(including) and ending with "/END"(excluding)
echo Removing old footers
for /r %%i in (*.ls) do (CALL "%~dp0\lib\JREPL\JREPL.BAT" "(\/POS\r\n)([\s\S]*)(\/END\r\n)" "$3" /B /M /F %%i /O %__localFtpDirectory%\%%~ni.tmp3 && move /Y "%%~ni.tmp3" "%%~i" >nul || echo -Error moving %%~ni.tmp3 to %%~ni.LS)

endlocal
echo FINISHED NORMALIZING
echo.