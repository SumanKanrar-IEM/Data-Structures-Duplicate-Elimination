class MySqlException(Exception):
	"""
	Custom Exception Class to handle exceptions
	"""
	def __init__(self, arguments):   # constructor accepting Exception in "arguments"
		self.message = arguments  # Stores the Exception in the message variable of the MySqlException Class
