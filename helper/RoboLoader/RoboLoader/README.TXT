*******************************************************************************
***** RoboLoader  *************************************************************
*******************************************************************************
Version: 1.0.0
Date: 12.8.2019

This is a set of batchfiles to exchange files from and to any fanuc robot.
Provides functions to compile .ls and .kl files to .tp and .pc as well.


///////////////////////////////////////////////////////////////////////////////
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
How to use
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
///////////////////////////////////////////////////////////////////////////////

Just copy the whole RoboLoader folder into the project root folder or whereever
you want it. The batch files will operate relative to this RoboLoader directory

Execute the .bat files to automatically exchange files from and to any robot.
What robots are part of the project as well as which robot is currently active
is defined in robotEnv.json. You can change the active robot with
___chooseActiveRobot.bat or enter it directly into robotEnv.json.

Lets say the currently active robot is "RoboGuide". When you
run _downloadAoa.bat the everything (and additional some setup stuff)
in ./FtpCommandFiles/aoaWinScpDownloadCommands.txt will be executed. The files
will be put in the robot base folder (defined in roboEnv.json) and there inside
of a folder with the name of the active robot. Inside this robot folder
are individual folders for each kind of backup.

///////////////////////////////////////////////////////////////////////////////
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
Extensions and Plugins
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
///////////////////////////////////////////////////////////////////////////////

If you want an easier way to run all the batchfiles in Atom you can extract
process-palette.json to its parent folder. Open this folder with the Atom
editor. You can now execute all the batch files from inside Atom. You should 
have a new menu tab called "RoboLoader" next to "Help". This requires the 
"process-palette" package to be installed.

If you use Visualstudio code then there is an extension that you can use as well.
Copy https://subversion.monnier-zahner.ch/svn/projects/FanucRobot/RoboLoader
into your C:\Users\deinBenutzer\.vscode\extensions. If you have placed the
RoboLoader folder in the folder that you open with vscode it will allow you
to execute the batch files more quickly. 
ctrl+shift+P and type RoboLoader to see all available commands.

With both options the RoboLoader folder still needs to be copied into every 
project that you want to use it in. The process-palette.json and the vsc
extension provide only shortcuts and have no code of themselves.

*******************************************************************************
**************** downloadXyz **************************************************
*******************************************************************************
* Gets an XYZ backup from the active robo. Will be put into folder named xyz.
* Which files are included is defined
* in ./FtpCommandFiles/xyzWinScpDownloadCommands.txt
*
* Using the line "set backupType=xyz" you can change what ftp commands will be
* executed and which folder they files will be stored/uploaded from.
*******************************************************************************

*******************************************************************************
**************** uploadXyz ****************************************************
*******************************************************************************
* Uploads files to the active robo. The files will be taken from folder
* named xyz. Which files are included is defined
* in ./FtpCommandFiles/xyzWinScpUploadCommands.txt
*
* Using the line "set backupType=xyz" you can change what ftp commands will be
* executed and which folder they files will be stored/uploaded from.
*
* Sometimes with upload commands that are only needed to setup a new robot and
* where data may be lost a confirmation prompt is shown.
*
* The line "set _localFtpDirectory=%robotsBaseFolder%\%activeRobot%\%backupType%"
* is sometimes set to use a specific folder instead of %backupType%. In some
* cases it makes sense to do this, e.g. if one set of files is technically
* a subset of another and its undesirable to have them in a seperate folder.
*******************************************************************************

*******************************************************************************
**************** compileSource ************************************************
*******************************************************************************
* Compiles all .ls files in the "source" folder to .tp files and puts them into
* the "bin" folder. Uses maketp.exe from WinOLPC. robot.ini needs to be in the
* same directory as batch files. If it's missing or needs to be updated use
* setrobot.exe from the lib folder.
*
* Using the first two variables (set X=???) in the .bat file you can change:
* - where the .ls files are found
* - to which folder the compiled .tp files will be saved
*******************************************************************************

*******************************************************************************
**************** compileKarelSource *******************************************
*******************************************************************************
* Compiles all .KL files in the "karelSource" folder to .PC files and puts them
* into the "karelBin" folder. Uses ktrans.exe from WinOLPC. robot.ini needs to
* be in the same directory as batch files. If it's missing or needs to be 
* updated use setrobot.exe from the lib folder. Otherwise a default compiler is 
* used
*
* Skips files with the ending .*.KL, which can be used for header files and 
* constants or similar files that cant be compiled themselves.
*
* Using the first two variables (set X=???) in the .bat file you can change:
* - where the .KL files are found
* - to which folder the compiled .PC files will be saved
*******************************************************************************

///////////////////////////////////////////////////////////////////////////////
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
Troubleshooting
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
///////////////////////////////////////////////////////////////////////////////

Windows firewall may cause problems.

If this folder is placed in a Path with spaces or if the robotsBaseFolder 
defined in robotEnv.json has spaces then the batch files might not work.

FTP and TCP/IP on robots needs to be configured right
("Menu">>"Setup">>"Host Comm." on Teaching pendant).

When trying to access a local Robot simulated in RoboGuide via FTP other FTP
servers on Port 21 (for example the service "Microsoft-FTP-Dienst") need to be
turned off. Afterwards RoboGuide needs to be restarted so that the ftp server
can be started correctly.
