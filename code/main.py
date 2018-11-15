from SqlException import MySqlException  # Imports the MySqlException Class which we defined for Exception Handling

import sys

"""
Importing the btree and hash file codes here
"""
import btree
import hash


# def debug(*args):
#     for each in args:
#         print args


def main():
    try:
        if len(sys.argv) < 6:  # If number of arguments passed is less than 6, then raise Exception
            raise MySqlException(
                "Usage: python main.py filename numAttributes~3 numBuffers~10 blockSize~144 typeOfIndex")
        elif sys.argv[4] == 0 or sys.argv[5] == "btree":  # Checking if argument "btree" is passed
            btree.distinct(sys.argv[1:-1])
            """
            Calls distinct function of btree by passing the arguments
            (absoluteFilePath/input_file, no_of_blocks, no of attributes, block_size)
            """
        elif sys.argv[4] == 1 or sys.argv[5] == "hash":  # Checking if argument "hash" is passed
            hash.distinct(sys.argv[1:-1])
            """
            Calls distinct function of btree by passing the arguments
            (absoluteFilePath/input_file, no_of_blocks, no of attributes, block_size)
            """

    except MySqlException, e:
        print e.message  # Prints the Exception Message


if __name__ == '__main__':
    main()
