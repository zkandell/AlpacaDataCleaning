import json
from Query import Query

def importandparseinstructions(filename):
    # Import the data as a list of dictionaries
    data = json.load(open(filename))
    # Change the data to a list of Query objects
    # The data is a list of dictionaries
    # Each dictionary is a single request with three parts
    # The first is the instruction to the bot
    # The second is the input (if needed)
    # The third is the output that the bot gave
    data = [Query(item["instruction"], item["input"], item["output"]) for item in data]
    # Return the data
    return data

def querylisttoformattedstring(querylist):
    # Convert a list of queries to a string
    # This is used to write the formatted data to a file
    retstr = ''
    for query in querylist:
        retstr += str(query)
    return retstr