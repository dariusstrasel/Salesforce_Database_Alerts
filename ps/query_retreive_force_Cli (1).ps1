function Parse-Query-File
{

param ($ImportFile)

$ImportFile = './test_output.txt'
$text = Import-Csv $ImportFile -Delimiter ',' 
$RecordCount = $text.Count
$myArray = @()
$i = 0

cls

$tabName = “SampleTable”

#Create Table object
$table = New-Object system.Data.DataTable “$tabName”


#Define Columns
$col1 = New-Object system.Data.DataColumn Account,([string])
$col2 = New-Object system.Data.DataColumn RuleName,([string])
$col3 = New-Object system.Data.DataColumn RecordCount,([string])

#Add the Columns
$table.columns.add($col1)
$table.columns.add($col2)
$table.columns.add($col3)

for ($it = 0; $it -le $RecordCount - 2; $it++) {
        
        $row = $table.NewRow()
        
        $row.Account = $text[1+$it].H1    
        $row.RuleName = $text[2+$it].H1   
        $row.RecordCount = $text[3+$it].H1
    
        #Add the row to the table
        $table.Rows.Add($row)     
        $it = $it + 2
    }

    
#Display the table
$table | Export-Csv -delimiter ',' -append 'output_query_file.csv'  -notype
}

############## END OF FUNCTIONS #####################

############## BEGIN RUNNING QUERIES ################

Set-Location "C:\Users\vgebhart\Documents\"
$OutputDirectory > test.txt

Get-Date > test_output.txt
$ImportFile = './accounts.csv'
$queries = New-Object System.Collections.ArrayList
    $queries.Add('SELECT COUNT(SFDCID__C) IsActiveTrue_Status_Not_Active FROM Contact where (mxw__Is_Active__c = true and Status__c != ''Active'')')
    $queries.Add('SELECT COUNT(SFDCID__C) IsActiveFalse_Status_Active FROM Contact where (mxw__Is_Active__c = false and Status__c = ''Active'')')
#Import Account csv and parse
$accounts = Import-Csv $ImportFile -Delimiter ','

$username = @{}
foreach ($account in $accounts) {
  $username[$account.'username'] = $account.pw
}

foreach ($query in $queries) 
    {
    
        $username.GetEnumerator() | % {
   
        
        .\force login -u $_.Name -p $_.Value >> test.txt
        .\force active -a $_.Name >> test.txt
            $_.Name >> test_output.txt
            'Current Account Parameter : ' + $_.Name  + '     ' + (Get-Date).ToString() >> test.txt
            'Prior Logged In Account : ' + (.\force active) + '   ' + (Get-Date).ToString() >> test.txt

            .\force query $query --format:csv >> test_output.txt
            'Current Logged In Account : ' + (.\force active) + '   ' + (Get-Date).ToString() >> test.tx
                                       }
    }

Parse-Query-File('./test_output.txt')

########### START EMAILING RESULTS ###############
$Results = Import-CSV -delimiter ',' .\output_query_file.csv | where RecordCount -gt 0

foreach($row in $results)
{
    $message += $row.Account + ' has failed rule ' + $row.RuleName + ' by ' + $row.RecordCount + ' records'+ "`n"
}

echo $message
