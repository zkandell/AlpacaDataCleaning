# Libraries to import
import json
import random

# Import from other files in this project
from Query import Query
from WordList import WordList
from importandexport import importandparseinstructions, querylisttoformattedstring
from finditemswithword import findInstruction

# Set the file name
filename = 'alpaca_data.json'

# Load the data
data = importandparseinstructions(filename)

# Create the list of stems that mark a query as irrelevant
# Use rarely, as this is slower and more ruthless than going by word lists
# This is most useful for removing things like links, which have a big obvious "http" at the front
# Any query that has any word that starts with any of the stems in the list will be removed, so be careful
stem_list = [
    'http'
]

def cleanandpartitiondata(data,inputpreference=None):
    # Clean the data by removing items without an output
    data = [item for item in data if not item.emptyoutput()]

    # Input preference is used to determine whether to remove items with an input or without an input
    # By default, it is None, which means to do nothing
    # If it is True, it will remove items without an input
    # If it is False, it will remove items with an input
    # If inputpreference is TRUE, remove items without an input
    if inputpreference:
        data = [item for item in data if not item.emptyinput()]
    # If inputpreference is FALSE, remove items with an input
    elif inputpreference == False:
        data = [item for item in data if item.emptyinput()]
    # If inputpreference is None, do nothing
    else:
        pass

    # Load the word lists
    yeswords = WordList("yeswords.txt")
    nowords = WordList("nowords.txt")

    # Create lists for queries to keep, to remove, and to maybe
    keep = []
    remove = []
    maybe = []

    # Loop through each item
    for item in data:
        # Check if the item fits the yes criteria
        if yeswords.checkquery(item):
            # If it does, add it to the keep list
            keep.append(item)
        # Check if the item fits the no criteria
        elif nowords.checkquery(item):
            # If it does, add it to the remove list
            remove.append(item)
        else:
            # Otherwise, add it to the maybe list
            maybe.append(item)

    # Check the yes and maybe lists for items that contain stems in the stem list
    # If they do, add them to the remove list and remove them from the yes and maybe lists
    for item in keep + maybe:
        if item.checkforstems(stem_list):
            remove.append(item)
            if item in keep:
                keep.remove(item)
            if item in maybe:
                maybe.remove(item)

    # Print the number of items in each list
    print(len(keep))
    print(len(maybe))
    print(len(remove))

    # Return the lists
    return keep, maybe, remove

def regenerateformatteddatafiles(data):
    keep,maybe,remove = cleanandpartitiondata(data)

    # The file names
    keepfilename = 'keep.txt'
    removefilename = 'remove.txt'
    maybefilename = 'maybe.txt'

    # Convert the lists of queries to properly formatted strings
    keepstr = querylisttoformattedstring(keep)
    removestr = querylisttoformattedstring(remove)
    maybestr = querylisttoformattedstring(maybe)

    # Write the lists to files
    with open(keepfilename, 'w',encoding='utf-8') as file:
        file.write(str(keepstr))
    with open(removefilename, 'w',encoding='utf-8') as file:
        file.write(str(removestr))
    with open(maybefilename, 'w',encoding='utf-8') as file:
        file.write(str(maybestr))

# Creates the text file used for training the bot
# This contains all of the items in the keep list
# It is then padded out to the character limit with random items from the maybe list
def buildfinaltextfile(data, filename='final.txt', charlimit=10000000, padtocharlimit=True, noisy=True):
    # Clean the data and partition it into lists
    keep,maybe,remove = cleanandpartitiondata(data)

    # Get the number of characters in the keep list
    keepcharcount = sum([item.charcount for item in keep])

    # Check to see if the keep list is already at or over the character limit
    if keepcharcount > charlimit:
        raise Exception("TOO MUCH GOOD DATA; the keep list is already over the character limit")

    # Determine how many characters are left after adding the keep list
    remaining = charlimit - len(querylisttoformattedstring(keep))
    
    def refreshmaybelist(maybe=maybe, remaining=remaining):
        # Refresh the maybe list by removing items that are too big
        # This is used to avoid code duplication
        # Remove items that are too big
        maybe = [item for item in maybe if item.charcount <= remaining]
        # If the maybe list is empty, return
        if len(maybe) == 0:
            return
        # Determine the size of the smallest and largest items in the maybe list
        global minsize, maxsize
        minsize, maxsize = maybe[0].charcount, maybe[0].charcount
        for item in maybe:
            if item.charcount < minsize:
                minsize = item.charcount
            if item.charcount > maxsize:
                maxsize = item.charcount

    def additemtokeep(item, keep=keep, maybe=maybe):
        # Add an item to the keep list
        # This function is used to avoid code duplication
        keep.append(item)
        maybe.remove(item)
        # Return the character count of the item (so that it can be subtracted from the remaining character count)
        return item.charcount

    # Refresh the maybe list
    refreshmaybelist(maybe, remaining)

    # Check to see if the maybe list is empty; if so, turn off padding, since there is nothing to pad with
    if len(maybe) == 0:
        padtocharlimit = False

    # Pad the keep list to the character limit with random items from the maybe list
    if padtocharlimit:
        # Loop until no more items can be added
        while remaining > minsize:
            # Get a random item from the maybe list
            item = random.choice(maybe)
            # Add it to the keep list and get its character count
            chars = additemtokeep(item)
            # Subtract its character count from the remaining character count
            remaining -= chars
            # Refresh the maybe list
            refreshmaybelist(maybe, remaining)
            # Print diagnostics (if noisy is True)
            if noisy:
                # Print the number of characters remaining
                print(remaining)
                # Print the length of the longest item in the maybe list
                print(maxsize)
            # Break if the maybe list is empty
            if len(maybe) == 0:
                break

    # Convert the keep list to a properly formatted string
    keepstr = querylisttoformattedstring(keep)

    # The file name
    finalfilename = filename

    # Write the keep list to the file
    with open(finalfilename, 'w',encoding='utf-8') as file:
        file.write(str(keepstr))

# Creates the json file used for training the bot
# This contains all of the items in the keep list
# Currently, it does not pad the file to a certain size
def buildfinaljsonfile(data):
    # Clean the data and partition it into lists
    keep, maybe, remove = cleanandpartitiondata(data)

    # The file name
    finalfilename = 'final.json'

    # Create the empty file (to be appended to later)
    # This is done to avoid having to load the entire file into memory
    open(finalfilename, 'w').close()

    # Loop through each item in the keep list
    for item in keep:
        # Write the item to the file as json
        with open(finalfilename, 'a') as file:
            file.write(json.dumps(item.to_json()) + "\n")

# regenerateformatteddatafiles(data)
# buildfinaltextfile(data, charlimit=10000000, padtocharlimit=True)