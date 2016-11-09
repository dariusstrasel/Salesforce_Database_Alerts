#Set-Location "C:\Users\vgebhart\Desktop\Deployment MEtadata Work\scripts"
#./Parse-Query-File.ps1 './test_output.txt'

#function Parse-Query-File
#{

#parm ([csv]$ImportFile)

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

for ($it = 0; $it -le $RecordCount; $it++) {
        
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
#}