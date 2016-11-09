$i = 0
#$username = @{"mxw_integration@preventure.com.uat1" = "doesnotsuck1";"mxw_aaa@preventure.com" = "aaaforc3"}
$OutputDirectory
#Set-Location "C:\Users\vgebhart\Documents\salesforce_ant\sample\"
$ImportFile = './accounts.csv'
#$PackageXML = 'C:\Users\vgebhart\Documents\salesforce_ant\sample\package.xml'
#$PackageXMLBuild = 'C:\Users\vgebhart\Documents\salesforce_ant\sample\unpackaged\package.xml'
#Copy-Item $PackageXML $PackageXMLBuild

Set-Location "C:\Users\vgebhart\Documents\"
Get-Date | Tee-Object -file 'c:\temp\metadata_extract_log.txt'

#Import Account csv and parse
$accounts = Import-Csv $ImportFile -Delimiter ','

$username = @{}
foreach ($account in $accounts) {
  $username[$account.'username'] = $account.pw
}

$username.GetEnumerator() | % {
    
    #set destination path and check to see if it exists
    $OutputDirectory = 'C:\Users\vgebhart\Documents\metadatas_withUR\' + $_.Name 

    If (Test-Path $OutputDirectory) {
        Remove-Item $OutputDirectory -Recurse -Force} 
            
    #connect to salesforce with current user creds and pull metadata to \metadata folder (cannot configure that at this time https://goo.gl/y2Gyii)

        'Current Account Parameter : ' + $_.Name  + '     ' + (Get-Date).ToString() | Tee-Object -file 'c:\temp\metadata_extract_log.txt' -Append
        Get-Date | Tee-Object -file 'c:\temp\metadata_extract_log.txt' -Append

Copy-Item -Path "C:\Users\vgebhart\Documents\salesforce_ant\sample\build_clean.properties" -Destination "C:\Users\vgebhart\Documents\salesforce_ant\sample\build.properties" -Force

(Get-Content C:\Users\vgebhart\Documents\salesforce_ant\sample\build.properties).replace('<Insert your Salesforce username here>', $_.Name) | Set-Content C:\Users\vgebhart\Documents\salesforce_ant\sample\build.properties
(Get-Content C:\Users\vgebhart\Documents\salesforce_ant\sample\build.properties).replace('<Insert your Salesforce password here>', $_.Value) | Set-Content C:\Users\vgebhart\Documents\salesforce_ant\sample\build.properties

    $env:Path = "C:\Program Files (x86)\Intel\iCLS Client\;C:\Program Files\Intel\iCLS Client\;C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem;C:\WINDOWS\System32\WindowsPowerShell\v1.0\;C:\Program Files (x86)\Intel\Intel(R) Management Engine Components\DAL;C:\Program Files\Intel\Intel(R) Management Engine Components\DAL;C:\Program Files (x86)\Intel\Intel(R) Management Engine Components\IPT;C:\Program Files\Intel\Intel(R) Management Engine Components\IPT;c:\Program Files (x86)\Microsoft SQL Server\110\Tools\Binn\ManagementStudio\;c:\Program Files (x86)\Microsoft SQL Server\110\Tools\Binn\;c:\Program Files\Microsoft SQL Server\110\Tools\Binn\;c:\Program Files (x86)\Microsoft SQL Server\110\DTS\Binn\;C:\Program Files\nodejs\;C:\Program Files\Git\cmd;C:\Program Files (x86)\Skype\Phone\;%JAVA_HOME%\bin;%ANT_HOME%\bin;C:\Users\vgebhart\AppData\Local\Microsoft\WindowsApps;C:\Users\vgebhart\AppData\Roaming\npm;C:\Program Files\Java\jdk1.8.0_101\bin;C:\Users\vgebhart\Documents\apache-ant-1.9.7\bin";
 
    echo $_.Name
    Set-Location "C:\Users\vgebhart\Documents\salesforce_ant\sample\"
    ant retrieveUnpackaged | Tee-Object -file 'c:\temp\metadata_extract_log.txt' -Append
    Set-Location "C:\Users\vgebhart\Documents\"
    
        
    #'Current Logged In Account : ' + (.\force active) + '   ' + (Get-Date).ToString() >> test.txt

    #copy the items from the most recent pull and move to the specified directory
    Copy-Item -Path 'C:\Users\vgebhart\Documents\salesforce_ant\sample\retrieveUnpackaged\' -Destination $OutputDirectory -Recurse -Force  >> test.txt
    
    $metaDataFiles = Get-ChildItem -Path $OutputDirectory\objects\
    $xdoc = New-Object System.Xml.XmlDocument

        foreach ($metadataFile in $metaDataFiles)  {
            $xdoc.Load($metadataFile.FullName)    
            $managedFields = $xdoc.CustomObject.fields | ?{$_.fullName -like 'mxw__*'} 
            #| Tee-Object -file 'c:\temp\metadata_extract_log.txt' -Append
                foreach ($field in $managedFields){                    
                    $xdoc.CustomObject.RemoveChild($field)
                    echo $metadataFile.Name
                    echo "$OutputDirectory\" + $metadataFile.Name
                    $xdoc.Save("$OutputDirectory\objects\" + $metadataFile.Name)
                }
        }

    Remove-Item 'C:\Users\vgebhart\Documents\salesforce_ant\sample\retrieveUnpackaged\' -Force -Recurse

}

#Invoke-Expression "& 'C:\Users\vgebhart\Desktop\Deployment MEtadata Work\scripts\Migration Tool CLI Deploy Script_loop.ps1'"