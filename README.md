README
======

allObVer contents:
------------------


extractOdbVerCCMA.sh: A quick and dirty bash shell script to extract verification
                      statistics from a set of CCMA ODBs. The extraction process
                      relies on an installation of the ODB-API  software bundle.

processOdbVerCCMA.sh: A quick and dirty bash shell script to produce verification
                      statistics from input ODB-2 files. This script relies on 
                      an installation of the ODB-API  software bundle.

nam_38: odb_migrator SQLs for CY38 ODBs
nam_40: odb_migrator SQLs for CY40 ODBs

plotCountUaObsBar.py:      plot observation count bar chart
plotCountUaObsTs.py:       plot observation count time-series
plotVerAvgProfObsVar.py:   plot forecast verification profile
plotVerFcLengthObsVar.py:  plot forecast verification


README.md -- this file

Dependenices:
-------------
[Python]: https://www.python.org/ 
[ODB-API]: http://software.ecmwf.int/ODBAPI

Instructions:
-------------

1. Gather ODB information in to an aggregated ODB-2 file:
```
./extractOdbVerCCMA.sh -i <input-odb-directory> [-o <odb2-directory>]
```

2. Produce verification statistics from your aggregated ODB-2 file:
```
processOdbVerCCMA.sh -i <odb2-directory> -C -V
```

3. Plot your verification statistics using these minimal set of python scripts (plot*.py).
