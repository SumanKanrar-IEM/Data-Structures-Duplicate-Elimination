# Removing duplicates

Performing duplicate elimination for a given relation.

1) main.py, main program and according to index we need to use two executables will be executed:
   if index is through btree then btree code will be executed
   else hash code gets executed
2) btree.py
3) hash.py


# Execution

See <>.sh file: python code/main.py filePath numAttributes~3 numBuffers~10 blockSize~144 typeOfIndex

typeOfIndex : "btree" / "hash" (without quotes)

blockSize in bytes


# Output

Distinct tuples will be printed in output_btree.txt or output_hash.txt in the main folder.

<>_output in output folder file contains time in seconds to execute and number of unique records in the following order:


numBuffers		filename		 blockSize

03			 100MB_20percent       1048576

03           1MB_50percent         1048576

05           100MB_20percent       2097152

05           1MB_50percent         2097152

10           100MB_20percent        104857

10           1MB_50percent          104857


100MB_20percent file hasn't been uploaded because of the 50MB size limit of Github. FYI, it has 2621448 records. 

System specifications for the given output file:

Python 2.7

Note: Assistance from GeeksForGeeks & github@umeshksingla