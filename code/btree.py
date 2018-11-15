from SqlException import MySqlException  # Imports the MySqlException Class for Exception Handling
import itertools
import sys
import time

INT_SIZE = sys.getsizeof(int())  # Calculates size of 'int' in Python & stores in a variable


class BNode(object):
    """
	A B+ Tree Node
	"""

    def __init__(self, minimum_degree, leaf):
        """
		min_degree = minimum number of children a node must have, before splitting
		max_degree = maximum number of keys a node can have
		children = (list) this node's children
		keys = (list) keys present in this node
		leaf = (bool) true if this node is a leaf
		"""
        self.minimum_degree = minimum_degree  # 't'
        self.children = [None] * (2 * self.minimum_degree)  # array of BNodes
        self.keys = [None] * (2 * self.minimum_degree - 1)  # array of keys (int)
        self.leaf = leaf
        self.present = 0  # Flag variable to denote the presence of a node

    def insertNode(self, val):
        """
		insertion method for a node,
		assuming that node is not full
		"""
        i = self.present - 1
        if self.leaf:
            while i >= 0 and self.keys[i] > val:
                self.keys[i + 1] = self.keys[i]
                i -= 1
            self.keys[i + 1] = val
            self.present += 1
        else:
            """if the node is not a leaf"""
            while i >= 0 and self.keys[i] > val:
                i -= 1
            if (self.children[i + 1]).present == 2 * self.minimum_degree - 1:
                """if the child is full"""
                self.addKeyAndSplit(i + 1, self.children[i + 1])

                # it has one more key now, so we need to check if that is also smaller than val or not
                if self.keys[i + 1] < val:
                    # if smaller, we need to insert one place ahead
                    i += 1
            self.children[i + 1].insertNode(val)

    def searchNode(self, val):
        """
		search for the key k
		"""
        i = 0
        while i < self.present and val > self.keys[i]:
            i += 1

        if i < len(self.keys) and self.keys[i] == val:
            return self

        if self.leaf:
            return None

        return (self.children[i]).searchNode(val)

    def addKeyAndSplit(self, i, childNode):
        """
		splits the ith child of calling node into two, and moves one key and node to the new node,
		assuming that the child node is full i.e. have 2*min_degree-1 keys
		"""
        B = BNode(childNode.min_degree, childNode.leaf)

        B.present = self.minimum_degree - 1

        # copy the last t-1 (min_keys) keys of this children to B
        j = 0
        while j < self.minimum_degree - 1:
            B.keys[j] = childNode.keys[j + self.minimum_degree]
            j += 1

        # copy the last t children of this children to B
        if not childNode.leaf:
            j = 0
            while j < self.minimum_degree:
                B.children[j] = childNode.children[j + self.minimum_degree]
                j += 1

        # reduce the number of keys in that children
        childNode.present = self.minimum_degree - 1

        # create the space for new child
        j = self.present
        while j >= i + 1:
            self.children[j + 1] = self.children[j]
            j -= 1

        # link the new node to self's one of children
        self.children[i + 1] = B

        # find the location of new key and move all greater keys one index ahead
        j = self.present - 1
        while j >= i:
            self.keys[j + 1] = self.keys[j]
            j -= 1

        # middle key is the one which gets pushed upwards
        # copy the middle key of childNode to self
        self.keys[i] = childNode.keys[self.minimum_degree - 1]

        # increment count of keys in self
        self.present += 1


class BTree(object):
    """
	A BTree
	"""

    def __init__(self, minimum_degree):
        """
		min_degree = minimum number of keys a node must have, before splitting
		"""
        self.minimum_degree = minimum_degree  # Initializes the minimum degree
        self.root = None

    def insert(self, val):
        """
		insertion method for a tree
		"""
        if self.root is None:
            """ the tree is empty """
            B = BNode(self.minimum_degree, True)
            B.keys.insert(0, val)
            B.present = 1
            self.root = B
        else:
            """the tree is not empty"""

            # if root is full, then tree grows in height
            if self.root.present == 2 * self.minimum_degree - 1:

                B = BNode(self.minimum_degree, False)
                B.children.insert(0, self.root)

                # split thr old root and move 1 key to the new root
                B.addKeyAndSplit(0, self.root)

                # now new_node has 2 children now, check where to insert val
                i = 0
                if B.keys[0] < val:
                    i += 1
                (B.children[i]).insertNode(val)
                self.root = B

            else:
                """the node is not full, so insert into this node"""
                (self.root).insertNode(val)

    def search(self, val):
        """
		search function for a tree
		"""
        if self.root is None:
            return None
        return (self.root).searchNode(val)


def getNext(btree, line, records_per_block, output_buffer):
    """
	checks and inserts the next record to the output buffer
	"""

    val = hash(line)  # Converts each line of record into hash value

    if btree.search(val) is None:
        output_buffer.append(line)
        # If no duplicate is found, appends to the output buffer and inserts to the B+Tree
        btree.insert(val)

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

    mindegree = block_size // INT_SIZE - 1  # Calculates the minimum degree

    btree = BTree(mindegree)

    if num_buffers <= 1:  # Should be at least 2 because M-1 buffers will be used as input buffers
        raise MySqlException("Number of buffers should be greater than or equal to 2")

    records_per_block = block_size // (INT_SIZE * num_attrs)  # Calculates the records per block

    N = (num_buffers - 1) * records_per_block  # Total number of input records. (input buffers * records per block)

    start = 0
    out = open('output_btree.txt', 'w+');  # Opens the output file in write append mode
    with open(filename, 'r') as f:  # Opens input file to read

        for input_buffer in iter(lambda: list(itertools.islice(f, N)), []):  # anonymous function to traverse through the list of records of the input file
            for line in input_buffer:  # Traverses through each line of record
                line = line.strip()  # Removes trailing and leading white spaces
                line = line.strip('\n')  # Removes new line character
                if len(line.split(',')) != num_attrs:  # Check if all the lines have same number of attributes or not
                    raise MySqlException("All rows do not contain same number of attributes")
                output_buffer = getNext(btree, line, records_per_block, output_buffer)  # Gets the next set of records from the input file

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
