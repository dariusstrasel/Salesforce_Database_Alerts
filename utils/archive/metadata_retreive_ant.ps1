$i = 0
#$username = @{"mxw_integration@preventure.com.uat1" = "doesnotsuck1";"mxw_aaa@preventure.com" = "aaaforc3"}
$OutputDirectory
$ImportFile = './accounts_umaster.csv'
Set-Location "C:\Users\vgebhart\Documents\"

#Import Account csv and parse
$accounts = Import-Csv $ImportFile -Delimiter ','

$username = @{}
foreach ($account in $accounts) {
  $username[$account.'username'] = $account.pw
}

$username.GetEnumerator() | % {
    
    #set destination path and check to see if it exists
    $OutputDirectory = '.\metadatas\' + $_.Name 

    If (Test-Path $OutputDirectory) {
        Remove-Item $OutputDirectory -Recurse -Force} 
            
    #connect to salesforce with current user creds and pull metadata to \metadata folder (cannot configure that at this time https://goo.gl/y2Gyii)

        'Current Account Parameter : ' + $_.Name  + '     ' + (Get-Date).ToString() >> test.txt
        'Prior Logged In Account : ' + (.\force active) + '   ' + (Get-Date).ToString() >> test.txt

@"
# build.properties
#

# Specify the login credentials for the desired Salesforce organization
sf.username = mxw_cmx@preventure.com
sf.password = cmxforc3
#sf.sessionId = <Insert your Salesforce session id here.  Use this or username/password above.  Cannot use both>
#sf.pkgName = <Insert comma separated package names to be retrieved>
#sf.zipFile = <Insert path of the zipfile to be retrieved>
#sf.metadataType = <Insert metadata type name for which listMetadata or bulkRetrieve operations are to be performed>

# Use 'https://login.salesforce.com' for production or developer edition (the default if not specified).
# Use 'https://test.salesforce.com for sandbox.
sf.serverurl = https://login.salesforce.com

sf.maxPoll = 20
# If your network requires an HTTP proxy, see http://ant.apache.org/manual/proxy.html for configuration.
#

"@  > C:\Users\vgebhart\Documents\salesforce_ant\sample\build.properties

    $env:Path = "C:\Program Files (x86)\Intel\iCLS Client\;C:\Program Files\Intel\iCLS Client\;C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem;C:\WINDOWS\System32\WindowsPowerShell\v1.0\;C:\Program Files (x86)\Intel\Intel(R) Management Engine Components\DAL;C:\Program Files\Intel\Intel(R) Management Engine Components\DAL;C:\Program Files (x86)\Intel\Intel(R) Management Engine Components\IPT;C:\Program Files\Intel\Intel(R) Management Engine Components\IPT;c:\Program Files (x86)\Microsoft SQL Server\110\Tools\Binn\ManagementStudio\;c:\Program Files (x86)\Microsoft SQL Server\110\Tools\Binn\;c:\Program Files\Microsoft SQL Server\110\Tools\Binn\;c:\Program Files (x86)\Microsoft SQL Server\110\DTS\Binn\;C:\Program Files\nodejs\;C:\Program Files\Git\cmd;C:\Program Files (x86)\Skype\Phone\;%JAVA_HOME%\bin;%ANT_HOME%\bin;C:\Users\vgebhart\AppData\Local\Microsoft\WindowsApps;C:\Users\vgebhart\AppData\Roaming\npm;C:\Program Files\Java\jdk1.8.0_101\bin;C:\Users\vgebhart\Documents\apache-ant-1.9.7\bin";
 
    echo $_.Name
    Set-Location "C:\Users\vgebhart\Documents\salesforce_ant\sample\"
    ant retrieveUnpackaged
    Set-Location "C:\Users\vgebhart\Documents\"
        
    #    'Current Logged In Account : ' + (.\force active) + '   ' + (Get-Date).ToString() >> test.txt

    #copy the items from the most recent pull and move to the specified directory
    Copy-Item -Path 'C:\Users\vgebhart\Documents\salesforce_ant\sample\retrieveUnpackaged\' -Destination $OutputDirectory -Recurse -Force  >> test.txt
    Remove-Item 'C:\Users\vgebhart\Documents\salesforce_ant\sample\retrieveUnpackaged\' -Force -Recurse

}