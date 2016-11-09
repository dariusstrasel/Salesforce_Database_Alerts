$SourceFolder = 'C:\Users\vgebhart\Documents\metadatas\mxw_goldmaster@preventure.com\'
$SourceFile = 'package.xml'

$TargetFolder = 'C:\Users\vgebhart\Documents\metadatas\mxw_asc@preventure.com\'
$TargetFile = 'package.xml'

$SourceObject = Get-Content $SourceFolder$SourceFile
$TargetObject = Get-Content $TargetFolder$TargetFile

Compare-Object  $SourceObject $TargetObject -IncludeEqual | Out-File 'c:\temp\XMLCompare.txt'