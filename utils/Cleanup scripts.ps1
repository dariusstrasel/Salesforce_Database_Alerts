#Copy-Item 'c:\users\vgebhart\documents\metadatas\*' -recurse 'c:\users\vgebhart\documents\metadatas_master\profiles\'  -include '.profile' -verbose 

######### Profiles ########################

Copy-Item -Path c:\users\vgebhart\documents\metadatas\ -Filter *.profile -Destination c:\users\vgebhart\documents\metadatas_master\profiles\ -WhatIf -Force -Recurse

Get-ChildItem -Path c:\users\vgebhart\documents\metadatas\ -Filter *.profile -Recurse | %{ Copy-Item -Path $_.FullName -Destination c:\users\vgebhart\documents\metadatas_master\profiles\ -Force }


###################################

$profiles = Get-ChildItem -Path c:\users\vgebhart\documents\metadatas_master\profiles\ 

Set-Location "C:\Users\vgebhart\Documents\"
$ImportFile = './accounts.csv'
$accounts = Import-Csv $ImportFile -Delimiter ','

foreach ($account in $accounts) {
  foreach ($profile in $profiles) {
  $path = $account.username
    Copy-Item -Path C:\Users\vgebhart\Documents\metadatas_master\profiles\$profile -Destination "C:\Users\vgebhart\Documents\metadatas\$path\profiles\" -WhatIf
    Copy-Item -Path C:\Users\vgebhart\Documents\metadatas_master\profiles\$profile -Destination "C:\Users\vgebhart\Documents\metadatas\$path\profiles\" -Verbose
}
}

########## Report Types ######################

Copy-Item -Path c:\users\vgebhart\documents\metadatas\ -Filter *.reportType -Destination c:\users\vgebhart\documents\metadatas_master\reportTypes\ -WhatIf -Force -Recurse

Get-ChildItem -Path c:\users\vgebhart\documents\metadatas\ -Filter *.reportType -Recurse | %{ Copy-Item -Path $_.FullName -Destination c:\users\vgebhart\documents\metadatas_master\reportTypes\ -Force }

$reportTypes = Get-ChildItem -Path c:\users\vgebhart\documents\metadatas_master\reportTypes\ -Filter *.reportType -Recurse 
$reportTypes.name

foreach ($account in $accounts) {
  foreach ($reportType in $reportTypes) {
  $path = $account.username
    Copy-Item -Path C:\Users\vgebhart\Documents\metadatas_master\reportTypes\$reportType -Destination "C:\Users\vgebhart\Documents\metadatas\$path\reportTypes\" -WhatIf
    Copy-Item -Path C:\Users\vgebhart\Documents\metadatas_master\reportTypes\$reportType -Destination "C:\Users\vgebhart\Documents\metadatas\$path\reportTypes\" -Verbose
}
}

########## Roles Types ######################

Copy-Item -Path c:\users\vgebhart\documents\metadatas\ -Filter *.role -Destination c:\users\vgebhart\documents\metadatas_master\roles\ -WhatIf -Force -Recurse

Get-ChildItem -Path c:\users\vgebhart\documents\metadatas\ -Filter *.role -Recurse | %{ Copy-Item -Path $_.FullName -Destination c:\users\vgebhart\documents\metadatas_master\roles\ -Force }

$roles = Get-ChildItem -Path c:\users\vgebhart\documents\metadatas_master\roles\ -Filter *.role -Recurse 
$roles.Name

foreach ($account in $accounts) {
  foreach ($role in $roles) {
  $path = $account.username
    Copy-Item -Path C:\Users\vgebhart\Documents\metadatas_master\roles\$role -Destination "C:\Users\vgebhart\Documents\metadatas\$path\roles\" -WhatIf
    Copy-Item -Path C:\Users\vgebhart\Documents\metadatas_master\roles\$role -Destination "C:\Users\vgebhart\Documents\metadatas\$path\roles\" -Verbose
}
}

########## Layout Types ######################

Copy-Item -Path c:\users\vgebhart\documents\metadatas\ -Filter *.layout -Destination c:\users\vgebhart\documents\metadatas_master\layouts\ -WhatIf -Force -Recurse

Get-ChildItem -Path c:\users\vgebhart\documents\metadatas\ -Filter *.layout -Recurse | %{ Copy-Item -Path $_.FullName -Destination c:\users\vgebhart\documents\metadatas_master\layouts\ -Force }

$layouts = Get-ChildItem -Path c:\users\vgebhart\documents\metadatas_master\layouts\ -Filter *.layout -Recurse 
$layouts.name

foreach ($account in $accounts) {
  foreach ($layout in $layouts) {
  $path = $account.username
    Copy-Item -Path C:\Users\vgebhart\Documents\metadatas_master\layouts\$layout -Destination "C:\Users\vgebhart\Documents\metadatas\$path\layouts\" -WhatIf
    Copy-Item -Path C:\Users\vgebhart\Documents\metadatas_master\layouts\$layout -Destination "C:\Users\vgebhart\Documents\metadatas\$path\layouts\" -Verbose
}
}

######## 