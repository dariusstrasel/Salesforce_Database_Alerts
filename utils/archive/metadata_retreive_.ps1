$i = 0
#$username = @{"mxw_integration@preventure.com.uat1" = "doesnotsuck1";"mxw_aaa@preventure.com" = "aaaforc3"}
$OutputDirectory
$ImportFile = './accounts.csv'

#Import Account csv and parse
$accounts = Import-Csv $ImportFile -Delimiter ','

$username = @{}
foreach ($account in $accounts) {
  $username[$account.'username'] = $account.pw
}

$username.GetEnumerator() | % {
    
    #set destination path and check to see if it exists
    $OutputDirectory = '.\metadatas\' + $_.Name > test.txt

    If (Test-Path $OutputDirectory) {
        Remove-Item $OutputDirectory -Recurse -Force}  >> test.txt
            
    #connect to salesforce with current user creds and pull metadata to \metadata folder (cannot configure that at this time https://goo.gl/y2Gyii)

        'Current Account Parameter : ' + $_.Name  + '     ' + (Get-Date).ToString() >> test.txt
        'Prior Logged In Account : ' + (.\force active) + '   ' + (Get-Date).ToString() >> test.txt

    .\force login -u $_.Name -p $_.Value >> test.txt
    .\force active -a $_.Name >> test.txt
    .\force export >> test.txt
        
        'Current Logged In Account : ' + (.\force active) + '   ' + (Get-Date).ToString() >> test.txt

    #copy the items from the most recent pull and move to the specified directory
    Copy-Item -Path '.\metadata\' -Destination $OutputDirectory -Recurse -Force  >> test.txt
    Remove-Item '.\metadata\*' -Force -Recurse  >> test.txt
}

