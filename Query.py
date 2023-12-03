import re

# A class to hold a query from the Alpaca data
# A query consists of an instruction, an input, and an output
# The instruction is the request that the user made
# The input is supplementary information that the user provided 
# The output is the response that the system gave
# Input is optional, but instruction and output are required
# The query also has a set of words that are in the query
# The words are used to search for queries when looking for specific words

class Query:
    def __init__(self, instruction, input, output):
        self.instruction = self.sanitize_text(instruction)
        self.input = self.sanitize_text(input)
        self.output = self.sanitize_text(output)
        self.getwords()
        # The number of characters in the query when printed
        self.charcount = len(self.__str__())

    def __str__(self):
        retstr = "----\n"
        if not self.emptyinstruction():
            retstr += "Request: " + self.instruction + "\n"
        if not self.emptyinput():
            retstr += "Input: " + self.input + "\n"
        if not self.emptyoutput():
            retstr += "Output: " + self.output + "\n"
        return retstr
    
    def __repr__(self):
        return self.__str__()
    
    def to_json(self):
        return {
            "instruction": self.instruction,
            "input": self.input,
            "output": self.output
        }

    def sanitize_text(self,text):
        # Remove smart quotes and other weird characters
        replacements = {
            "\u2018": "'",  # left single quotation mark
            "\u2019": "'",  # right single quotation mark
            "\u201C": '"',  # left double quotation mark
            "\u201D": '"',  # right double quotation mark
            "\u2013": "-",  # en dash
            "\u2014": "--", # em dash
        }

        for weird_char, straight_char in replacements.items():
            text = text.replace(weird_char, straight_char)

        # Turn multiple spaces into a single space
        text = re.sub(r' +', ' ', text)

        # Turn multiple newlines into a single newline
        text = re.sub(r'\n+', '\n', text)

        # Remove leading and trailing whitespace
        text = text.strip()

        return text
    
    def emptyinstruction(self):
        return self.instruction == ""
    
    def emptyinput(self):
        return self.input == "" or self.input == "Noinput" or self.input == "<no input>"
    
    def emptyoutput(self):
        return self.output == "" or self.output == "<No output>"

    def getwords(self,instructonly=True):
        def cleanword(word):
            # Convert to lowercase
            word = word.lower()
            # Remove non-alphanumeric characters
            word = re.sub(r'[^\w\s]', '', word)
            # Return the word
            return word

        # Create a set to hold the words
        words = set()
        
        # Split the instructions into words
        instruct = self.instruction.split()
        # Clean up words from the instruction and add them to the word set
        words.update([cleanword(word) for word in instruct])
        # If instructonly is False, do the same for the input and output
        if not instructonly:
            input = self.input.split()
            output = self.output.split()
            words.update([cleanword(word) for word in input])
            words.update([cleanword(word) for word in output])

        # Remove the empty string from the word set
        words = {word for word in words if word != ""}

        # Save the word set
        self.words = words

    # Check if a given word is in the query
    def checkforword(self, word):
        searchword = word.lower()
        if searchword in self.words:
            return True
        else: 
            return False
        
    # Check if any of a given list of words is in the query
    def checkforwords(self, words):
        for word in words:
            if self.checkforword(word):
                return True
        return False
    
    # Check if any word in the query starts with a given stem
    def checkforstem(self, stem):
        searchstem = stem.lower()
        for word in self.words:
            if word.startswith(searchstem):
                return True
        return False
    
    # Check if any word in the query starts with any of a given list of stems
    def checkforstems(self, stemlist):
        for stem in stemlist:
            if self.checkforstem(stem):
                return True
        return False