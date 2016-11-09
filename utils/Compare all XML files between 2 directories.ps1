 cls
# Setup
#$Path1 = “C:\Users\vgebhart\Documents\salesforce_ant\sample\retrieveUnpackaged\objects\”

Set-Location "C:\Users\vgebhart\Documents\"
$ImportFile = './accounts.csv'
$foldername = @('objects','applications','dashboards','profiles','reports','reportTypes','roles','tabs','reports\Client_Reports')

#Import Account csv and parse
$accounts = Import-Csv $ImportFile -Delimiter ','

$username = @{}
foreach ($account in $accounts) {
  $username[$account.'username'] = $account.pw
}

$username.GetEnumerator() | % {
foreach ($folder in $foldername) {
$Path1 = “C:\Users\vgebhart\Documents\metadatas\mxw_goldmaster@preventure.com\$folder\”
$Path2 = “C:\Users\vgebhart\Documents\metadatas\" + $_.Name + "\$folder\"
#$Path1 = “C:\Users\vgebhart\Documents\metadatas\mxw_goldmaster@preventure.com\”
#$Path2 = “C:\Users\vgebhart\Documents\metadatas\" + $_.Name + "\"
$OutFile = “C:\temp\metadata_compare\" + $_.Name + ".txt"

 # Delete outfile if it exists
If (Test-Path($OutFile)) {Remove-Item $OutFile}

# Write the two paths to the outfile so you know what you’re looking at
#“Differences in files of the same name between the following folders: ” + $Path1 + ” AND ” + $Path2 | Out-File $OutFile 
 
 # Compare two folders and return only files that are in each
$Dir1 = Get-ChildItem -Path $Path1 -Recurse  
$Dir2 = Get-ChildItem -Path $Path2 -Recurse
$FileList = Compare-Object $Dir1 $Dir2 -IncludeEqual -ExcludeDifferent

# Loop the file list and compare file contents
ForEach ($File in $FileList)
{
    $Outfile = “C:\temp\metadata_compare_with_eq\" + $File.InputObject + "_" + $_.Name  + "_witheq.txt"
    $F1 = $Path1 + “\” + $File.InputObject
    $F2 = $Path2 + “\” + $File.InputObject
    $File.InputObject.name | Out-File $OutFile -append
    Compare-Object $(Get-Content $F1) $(Get-Content $F2) -IncludeEqual| Out-File $OutFile -width 1200 -append
}

Get-Content $OutFile
echo $OutFile
}
}