# Purpose: find instructions with a certain word
from importandexport import importandparseinstructions
from WordList import WordList

# Find instructions with a certain word in it
# @param word: the word to search for
# @param instructiononly: if True, only search in the instruction field
# @param instructionfile: the file to search in
# @param writetofile: if True, write the results to a file
# @param outputfilename: the name of the file to write to (if writetofile is True); if None, file name will default to {word}.txt
# @return: a list of instructions with the word in it
def findInstruction(word,instructiononly=True,instructionfile='alpaca_data.json',writetofile=True,outputfilename=None):
    # Get the queries
    allqueries = importandparseinstructions(instructionfile)
    # By default, queries only get the words for the instruction field
    # If instructiononly is False, we need to get the words for the other fields
    if not instructiononly:
        for query in allqueries:
            query.getwords(instructonly=False)
    # Search for the word in the queries
    foundqueries = []
    for query in allqueries:
        if query.checkforword(word):
            foundqueries.append(query)

    # Write the results to a file
    if writetofile:
        if outputfilename is None:
            outputfilename = word + '.txt'
        with open(outputfilename,'w',encoding='utf-8') as f:
            for query in foundqueries:
                f.write(str(query))

# Test the function
if __name__ == '__main__':
    findInstruction('write',writetofile=True)