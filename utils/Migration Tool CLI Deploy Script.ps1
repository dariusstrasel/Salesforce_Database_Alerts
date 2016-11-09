$SourceUserName = 'mxw_cmx@preventure.com'
$TargetUserName = 'mxw_deployment+umaster@preventure.com'
$password = 'l4gyP7pJCf7l'

$InputDirectory = '.\metadatas\' + $SourceUserName
$BuildDirectory = 'C:\Users\vgebhart\Documents\salesforce_ant\sample\retrieveUnpackaged\'

ECHO $InputDirectory

Copy-Item -Path "C:\Users\vgebhart\Documents\salesforce_ant\sample\build_clean.properties" -Destination "C:\Users\vgebhart\Documents\salesforce_ant\sample\build.properties" -Force
(Get-Content C:\Users\vgebhart\Documents\salesforce_ant\sample\build.properties).replace('<Insert your Salesforce username here>', $TargetUsername) | Set-Content C:\Users\vgebhart\Documents\salesforce_ant\sample\build.properties
(Get-Content C:\Users\vgebhart\Documents\salesforce_ant\sample\build.properties).replace('<Insert your Salesforce password here>', $password) | Set-Content C:\Users\vgebhart\Documents\salesforce_ant\sample\build.properties

$env:Path = "C:\Program Files (x86)\Intel\iCLS Client\;C:\Program Files\Intel\iCLS Client\;C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem;C:\WINDOWS\System32\WindowsPowerShell\v1.0\;C:\Program Files (x86)\Intel\Intel(R) Management Engine Components\DAL;C:\Program Files\Intel\Intel(R) Management Engine Components\DAL;C:\Program Files (x86)\Intel\Intel(R) Management Engine Components\IPT;C:\Program Files\Intel\Intel(R) Management Engine Components\IPT;c:\Program Files (x86)\Microsoft SQL Server\110\Tools\Binn\ManagementStudio\;c:\Program Files (x86)\Microsoft SQL Server\110\Tools\Binn\;c:\Program Files\Microsoft SQL Server\110\Tools\Binn\;c:\Program Files (x86)\Microsoft SQL Server\110\DTS\Binn\;C:\Program Files\nodejs\;C:\Program Files\Git\cmd;C:\Program Files (x86)\Skype\Phone\;%JAVA_HOME%\bin;%ANT_HOME%\bin;C:\Users\vgebhart\AppData\Local\Microsoft\WindowsApps;C:\Users\vgebhart\AppData\Roaming\npm;C:\Program Files\Java\jdk1.8.0_101\bin;C:\Users\vgebhart\Documents\apache-ant-1.9.7\bin";

If(Test-Path($BuildDirectory)) {Remove-Item -Path 'C:\Users\vgebhart\Documents\salesforce_ant\sample\retrieveUnpackaged\' -Recurse -Force}
If(Test-Path($InputDirectory)) {Copy-Item -Path $InputDirectory\ -Destination 'C:\Users\vgebhart\Documents\salesforce_ant\sample\retrieveUnpackaged\' -Recurse -Force}

Set-Location "C:\Users\vgebhart\Documents\salesforce_ant\sample\"
ant deployUnpackaged
Set-Location "C:\Users\vgebhart\Documents\"