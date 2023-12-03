# A list of key words that are used to determine if a query is relevant to a given topic
# Despite the name, this is a dictionary, not a list
# The keys are key words, and the values are exceptions to the key word
# For example, the word "write" is a key word that is used to determine if a query is about writing
# However, the word "write" is also used in the instruction "write a program to calculate the sum of two numbers"
# In that case, "program" is an exception to the key word "write"
# This would be written in the file as "write program"
# Many of the key words will have no exceptions, but they are very useful when present
class WordList:
    def __init__(self,filename):
        self.filename = filename
        self.parsefile()

    # Parse a single line from the file
    def parseline(self,line):
        # Split the line into words
        words = line.split()
        # The first word is the key word
        keyword = words[0]
        # The rest of the words are exceptions
        exceptions = words[1:]
        # Return the key word and exceptions
        return keyword, exceptions

    def parsefile(self):
        # Loading and cleaning up the word list
        # Load the file as a list of lines
        lines = open(self.filename).readlines()
        # Remove any line that starts with a # (comments)
        lines = [line for line in lines if not line.startswith("#")]
        # Remove any line that is empty or only contains whitespace
        lines = [line for line in lines if not line.isspace()]
        # Strip the whitespace from the beginning and end of each line
        lines = [line.strip() for line in lines]

        # Create a dictionary to hold the key words and exceptions
        self.wordlist = {}

        # Loop through each line
        for line in lines:
            keyword, exceptions = self.parseline(line)
            # Add the key word and exceptions to the dictionary
            self.wordlist[keyword] = exceptions

    # Check if a given query matches this list
    # This is done by checking if the query contains any of the key words
    # If it does, it checks if it contains any of the exceptions
    # If it does not, it returns True
    # If it does, it returns False
    # Must be called on a Query object, not a string
    # Uses the Query.checkforword() and Query.checkforwords() methods, which do not exist on strings
    def checkquery(self, query):
        # Loop through each key word
        for keyword in self.wordlist:
            # Get the exceptions for this key word
            exceptions = self.wordlist[keyword]
            # Check if the query contains the key word
            if query.checkforword(keyword):
                # If the query contains the key word, check if it contains any of the exceptions
                if query.checkforwords(exceptions):
                    # If it contains an exception, return False
                    return False
                else:
                    # If it does not contain an exception, return True
                    return True
        # If the query does not contain any of the key words, return False
        return False