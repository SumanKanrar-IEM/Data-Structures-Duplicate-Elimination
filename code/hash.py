from SqlException import MySqlException  # Imports the MySqlException Class for Exception Handling
import itertools
import sys
import time

hashmap = {}  # Declares a blank Python Set

INT_SIZE = sys.getsizeof(int())  # Calculates size of 'int' in Python & stores in a variable


def getNext(line, records_per_block, output_buffer):
    """
	checks and inserts the next record to the output buffer
	"""

    sum = hash(line)  # Converts each line of record into hash value

    try:
        val = hashmap[sum]
    except:
        hashmap[sum] = line
        output_buffer.append(line)  # Adds record to the output buffer

    return output_buffer  # Returns the output buffer and further checks whether it is full or not


def openfile(filename, num_attrs, num_buffers, block_size):
    """
	open the file, read a chunk at a time, take a line from it and check whether it is duplicate or not, 
	empty the output buffer when filled by flushing, and
	then closes the file
	"""

    output_buffer = []  # Blank List for output buffer

    block_size = int(block_size)  # Converts block size to Integer
    num_attrs = int(num_attrs)  # Converts number of attributes to Integer
    num_buffers = int(num_buffers)  # Converts number of buffers(blocks) to Integer

    if num_buffers <= 1:  # Should be at least 2 because M-1 buffers will be used as input buffers
        raise MySqlException("Number of buffers should be greater than or equal to 2")

    records_per_block = block_size // (INT_SIZE * num_attrs)  # Calculates the records per block

    N = (num_buffers - 1) * records_per_block  # Total number of input records. (input buffers * records per block)

    start = 0
    out = open('output_hash.txt', 'w+');  # Opens the output file in write append mode

    with open(filename, 'r') as f:  # Opens input file to read

        for input_buffer in iter(lambda: list(itertools.islice(f, N)), []):  # anonymous function to traverse through the list of records of the input file
            for line in input_buffer:  # Traverses through each line of record
                line = line.strip()  # Removes trailing and leading white spaces
                line = line.strip('\n')  # Removes new line character
                if len(line.split(',')) != num_attrs:  # Check if all the lines have same number of attributes or not
                    raise MySqlException("All rows do not contain same number of attributes")
                output_buffer = getNext(line, records_per_block, output_buffer)  # Gets the next set of records from the input file

                if len(output_buffer) == records_per_block:
                    """
                    If output buffer is full, it should be flushed to the output file and output buffer should be emptied
                    """
                    a = '\n'.join(output_buffer)
                    out.write(a + '\n')
                    output_buffer = []

        if len(output_buffer):
            a = '\n'.join(output_buffer)
            out.write(a + '\n')
            output_buffer = []
        out.close()  # Close the output file after writing


def distinct(args):
    """
        This is the main entry point the code from the main file.
	"""
    start_time = time.time()  # Stores the start time
    openfile(args[0], args[1], args[2], args[3])  # Control goes to openfile function with the respective parameters
    print("%s sec" % (time.time() - start_time))  # Prints how much time it took to run the whole processing
