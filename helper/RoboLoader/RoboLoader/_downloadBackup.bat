::######################################################
::# Downloads all needed backup types for an easy
::# easy to handle backup. 
::######################################################

::BackupSequence
CALL %~dp0\_downloadAoa.bat CONT
CALL %~dp0\_downloadConfig.bat CONT
CALL %~dp0\_downloadSource.bat CONT

ECHO SCRIPT FINISHED
if [%1]== PAUSED (pause)
if [%1]== STOP (cmd /k)
if [%1]== CONT (exit /B)
if [%1]==[] (cmd /k)
