#!/bin/tcsh

set dirin = $*
foreach i (`ls -1 "$dirin" | grep .root | awk '{print $NF}'`)

echo "'file:"$dirin$i"',"

end

