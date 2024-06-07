import socket, sys, time

def listen(ip,port, newFolder):
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

                    $hname=hostname
                    $date=Get-Date -Format \"yyyyMMdd\"
                    $env:backupFolderName=$hname+\"_\"+$date

                    $backupFolder = $dl+"\\CNC\\"+$env:backupFolderName
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
                    New-Item -Path $backupFolder\"_\"$backupFolderNr -ItemType Directory | Out-Null
                    echo \"Backup folder created \"

                    $SourcePath = $dl+"\\CNC\\TEMP"
                    $DestinationPath = $backupFolder+\"_\"+$backupFolderNr

                    # Get all the files and subdirectories in the source directory
                    $Items = Get-ChildItem -Path $SourcePath

                    # Loop through each item and move it to the destination directory
                    foreach ($Item in $Items)
                    {
                        Move-Item -Path $Item.FullName -Destination $DestinationPath
                    }
                    
                    #copy log file
                    Move-Item -Path "C:\\ProgramData\\FANUC\\CNCDataManagementTool\\Log\\$date.Log" -Destination $backupFolder\"_\"$backupFolderNr
                    """
    command += "\n"
    conn.sendall(command.encode())
	
    #Receive data from the target and get user input
    #while True:
    try:
        ans = conn.recv(1024).decode()
        #if not ans: break
        sys.stdout.write(ans)
    except:
        sys.stdout.write("An exception occurred") 
    s.close()
    # s.shutdown(1) # gives bad file descriptor error