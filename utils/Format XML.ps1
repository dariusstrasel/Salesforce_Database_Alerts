$FileLocation = '.\salesforce_ant\sample\retrieveUnpackaged\objects\Account.object'

$Content = Get-Content $FileLocation -Raw
#$Output = Replace($Content, "<fields>\s*<fullName>mxw__.*?<\/fields>",'');

$Content = $Content -replace '$CancelEdit$','a'

Format-XML $Content >> c:\temp\test.xml

