$ImportFile = 'c:\temp\exclusion_list.csv'
$OutputDirectory = 'C:\Users\vgebhart\Documents\metadatas\mxw_bosch@preventure.com'
#Import AExclusion_List.csv and parse
$Exclusion_List = Import-Csv $ImportFile -Delimiter ','

$Exclusion_List

foreach ($object in $Exclusion_List) {        
           
        $metaDataFiles = Get-ChildItem -Path $OutputDirectory\objects\
        $xdoc = New-Object System.Xml.XmlDocument

        $FilePath = $OutputDirectory + '\' + $object.folder + '\' + $metadataFile
        $FilePath
        $xdoc.Load($FilePath)
        $test = $object.parentnode

        
        $managedFields = $xdoc.$test | ?{$object.node -eq $object.element} 
        $managedFields
            #| Tee-Object -file 'c:\temp\metadata_extract_log.txt' -Append
                foreach ($field in $managedFields){                    
                    $xdoc.CustomObject.RemoveChild($field)
                    echo $metadataFile.Name
                    echo "$OutputDirectory\" + $metadataFile.Name
                    }
        #$xdoc.node.RemoveChild($object.node)
}

        

        #foreach ($metadataFile in $metaDataFiles)  {
            
            #if ($metadataFile = $object) {$xdoc.Load($FilePath)} Else {break}
            #$managedFields = $xdoc.CustomObject.fields | ?{$_.fullName -like 'mxw__*'} 
            #| Tee-Object -file 'c:\temp\metadata_extract_log.txt' -Append
            #    foreach ($field in $managedFields){                    
                    $xdoc.CustomObject.RemoveChild($field)
                    echo $metadataFile.Name
                    echo "$OutputDirectory\" + $metadataFile.Name
                    $xdoc.Save("$OutputDirectory\objects\" + $metadataFile.Name)
                }
        }   
            
        } 
    }
}

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