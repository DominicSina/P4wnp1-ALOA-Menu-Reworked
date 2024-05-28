import socket, sys, time

def listen(ip,port,activeRobot, newFolder):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip, port))
    s.listen(1)
    print("Listening on port " + str(port))
    conn, addr = s.accept()
    print('Connection received from ',addr)

    #Send command
    command = """$drivefound=$false
                    while (-not $drivefound)
                    {
                        try
                        {
                            $drive=Get-Volume -FileSystemLabel \"P4wnP1 ALOA\" -ErrorAction Stop
                        }
                        catch 
                        {
                            \"Waiting for P4wnP1 drive\"
                            sleep 1
                            continue
                        } 
                        $dl=($drive.DriveLetter | Out-String)[0] +\":\"
                        $drivefound=$true
                    }

                    $roboLoaderFolder = $dl+\"\\\\RoboLoader\"
                    if (Test-Path -Path $roboLoaderFolder ) {
                        echo \"RoboLoader found\"
                    } else {
                        echo \"RoboLoader not found\"
                        return
                    }

                    $hname=hostname
                    $date=Get-Date -Format \"yyyyMMdd\"
                    $env:backupFolderName=$hname+\"_\"+$date
                    $json = Get-Content $roboLoaderFolder\"\\\\robotEnv.json\" | ConvertFrom-Json

                    $backupFolder = $json.config.robotsBaseFolder
                    $backupFolder = $backupFolder.replace(\"%~dp0\\..\",$dl)
                    $backupFolder = $backupFolder.replace(\"%backupFolderName%\",$env:backupFolderName)
                    $backupFolderNr = 0
                    while ($true)
                    {
                        if (Test-Path -Path $backupFolder\"_\"$backupFolderNr) {
                            $backupFolderNr = $backupFolderNr + 1
                        } else {"""+("""
                            if($backupFolderNr -gt 0){
                                $backupFolderNr = $backupFolderNr - 1
                            }""" if not newFolder else """""")+"""
                            $env:backupFolderName=$env:backupFolderName+\"_\"+$backupFolderNr
                            break
                        }
                    }
                    
                    #batch files will create folder but log files of start-process are created first and need an existing path
                    New-Item -Path $backupFolder\"_\"$backupFolderNr\\\\"""+activeRobot+""" -ItemType Directory | Out-Null
                    Start-Process -FilePath $dl\"\\\\RoboLoader\\\\___chooseActiveRobot.bat\" -ArgumentList """+activeRobot+""" -Wait -RedirectStandardOutput $backupFolder\"_\"$backupFolderNr\\\""""+activeRobot+"""\\stdoutChooseActiveRobot.txt\" -RedirectStandardError $backupFolder\"_\"$backupFolderNr\\\""""+activeRobot+"""\\stderrChooseActiveRobot.txt\"
                    
                    $process = Start-Process -FilePath $dl\"\\\\RoboLoader\\\\_downloadCompleteBackup.bat\" -ArgumentList \"CONT\" -PassThru -RedirectStandardOutput $backupFolder\"_\"$backupFolderNr\\\""""+activeRobot+"""\\stdoutDownloadCompleteBackup.txt\" -RedirectStandardError $backupFolder\"_\"$backupFolderNr\\\""""+activeRobot+"""\\stderrDownloadCompleteBackup.txt\"
                    
                    # https://stackoverflow.com/questions/69652895/process-standardoutput-readline-is-hanging-when-there-is-no-output
                    # Open the file for reading, and convert it to a System.IO.StreamReader instance.
                    [IO.StreamReader] $reader = [IO.File]::Open($backupFolder+\"_\"+$backupFolderNr+\"\\"""+activeRobot+"""\"+\"\\stdoutDownloadCompleteBackup.txt\", \'Open\', \'Read\', \'ReadWrite\')
                    try {
                        $task = $reader.ReadLineAsync() # Start waiting for the first line.
                        while ($true) { # Loop indefinitely to wait for new lines.
                            if ($task.IsCompleted) {  # A new line has been received.
                                $res = $task.Result;
                                if (-not ([string]::IsNullOrEmpty($res))) {
                                    # Output
                                    # echo $res
                                    Write-Host $res
                                }
                                # Start waiting for the next line.
                                $task.Dispose(); $task = $reader.ReadLineAsync();
                            }
                            else { # No new line available yet, do other things.
                                Start-Sleep 3
                            }
                            # stop pulling lines from file if processes has ended
                            if($process.HasExited){
                                break
                            }
                        }
                    }
                    finally {
                        $reader.Dispose()
                    }
                    
                    echo \"Backup finished or aborted\""""
    command += "\n"
    conn.send(command.encode())
    #conn.sendall(command.encode())
    
    
    #Receive data from the target and get user input
    ans = conn.recv(1024).decode()
    sys.stdout.write(ans)
    s.close()
    #while True:
    #    try:
    #        ans = conn.recv(1024).decode()
    #        if not ans: break
    #        sys.stdout.write(ans)
    #    except:
    #        sys.stdout.write("An exception occurred")
    
    # s.shutdown(1) # gives bad file descriptor error