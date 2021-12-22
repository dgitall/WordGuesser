import json
import random
from urllib.request import urlopen

# Load the string dictionary from the JSON file
StringDictionary = {}
with open('stringfile.json') as json_file:
    StringDictionary = json.load(json_file)

# Function to evaluate the loaded f-strings. This is necessary because you can't include
# dictionary keys if doing it inline due to interference with single and double quotes.
# Taken from: https://stackoverflow.com/questions/47597831/python-fstring-as-function
def fstr(fstring_text, locals, globals=None):
    """
    Dynamically evaluate the provided fstring_text
    """
    locals = locals or {}
    globals = globals or {}
    ret_val = eval(f'f"{fstring_text}"', locals, globals)
    return ret_val


## Open a file from a github repository containing a bunch of words
## Load this into our internal dictionary
def OpenDictionary():
    dictionary = dict()

    print(fstr(StringDictionary['LoadingDictionary'], locals()))
   
    with urlopen("https://github.com/dwyl/english-words/blob/master/words_alpha.txt?raw=true") as data:
        # Transform the bitstream into strings
        f = data.read()
        texts = f.decode(encoding='utf-8', errors='ignore')
        # Split up the text into a list of words
        lines = texts.split('\r\n')
        counter=0
        # Load the words into the dictionary
        for word in lines:
            dictionary[counter] = word
            counter+=1
  
    return dictionary

## Randomly pick a word from our dictionary for the user to guess
def SelectWord(dictionary):
    # Remove an arbitrary selection from the dictionary
    # Removing will ensure the word is not selected again
    randomKey = random.randint(0, len(dictionary))
    SelectedWord = str(dictionary.pop(randomKey))
    SelectedWord.lower()
    
    return SelectedWord

## Initialize the displaylist object which says which character of the word to display in the clue
def InitDisplayList(Word):
    # Initialize as the Word to get the right length
    DisplayList = list(Word)
    # Set all of the values to False so no characters are displayed
    for index, char in enumerate(Word):
        DisplayList[index] = False
    
    return DisplayList

## Display the clue with '_' in places where they haven't already guessed the character
## This is stored in the DisplayList as true where the word characters are shown
def ShowWord(Word, DisplayList):
    # Create the Displayed version of the word starting with the Word characters
    # Change to add '_' where DisplayList is False 
    # Convert to a list because strings are immutable 
    DisplayWord = list(Word)
    for index, char in enumerate(Word):
        if not DisplayList[index]:
            DisplayWord[index] = "_"
    # Convert the list back into a string after we are done changing values
    joined_string = " ".join(DisplayWord)
    rem_letters = len(DisplayList)-sum(DisplayList)
    # Show DisplayWord as a Clue
    print(fstr(StringDictionary['ClueMessage'], locals()))
    
## Check to see if UserInput matches any letters in Word. Where it does, se DisplayList to True
def CheckChar(Word, DisplayList, UserInput):
    # Go through all of the characters in the Word and turn on the display
    # for each that matches the User Input
    for index, char in enumerate(Word):
        if char == UserInput:
            DisplayList[index] = True


        
## Prompt the user for input and verify that it is a string and not empty.
def GetUserInput():
    UserInput = str()
    GetInput = True
    Message = StringDictionary['InputPrompt']
    
    while GetInput:
        # Prompt User Entry
        Entry = input(Message)
        # Is entry length > 0
        if len(Entry) <= 0:
            Message = StringDictionary['InputPrompt']
        else:
            # Is entry a string?
            if Entry.isnumeric():
                Message = StringDictionary['CharError']
            else:
                # Valid input received so exit the loop
                UserInput = Entry
                GetInput = False
    
    UserInput.lower()
    return UserInput
    
# Main Body
dictionary = OpenDictionary()

# Loop through playing the game until the user says to stop
PlayingGame = True
GameCount = 0
while PlayingGame:
    # Check to make sure that we haven't used up all of the words in our dictionary
    if len(dictionary) == 0:
        break
    # Select the word for the play to guess
    Word = SelectWord(dictionary)

    DisplayList = InitDisplayList(Word)

    TurnCounter = 0
    MaxTurns = 7
    WinCount = 0
    GameCount += 1
    GameMessage = StringDictionary['GameOver']
    SuccessMessage = StringDictionary['Success']
    ## Give the player 7 tries to guess the word. 
    while TurnCounter < 7:
        ## Display the clue
        print(fstr(StringDictionary['RoundMsg'], locals()))
        ShowWord(Word, DisplayList)
        # Get the users guess
        UserInput = GetUserInput()
        
        # If the user enters a single character check where it is in the word
        if(len(UserInput) == 1):
            # Check if character is in the word list
            CheckChar(Word, DisplayList, UserInput)
            # Check if all characters filled in the word
            if(sum(DisplayList) == len(DisplayList)):
                GameMessage = SuccessMessage
                WinCount += 1
                break
            TurnCounter += 1
        # If the user entered multiple characters this is a word guess 
        else:
            # Check if the guess is correct
            if UserInput == Word:
                GameMessage = SuccessMessage
                WinCount += 1
                break
            
    print(GameMessage + fstr(StringDictionary['ResultsMsg'], locals()))
    PlayAgain = input(StringDictionary['PlayAgain'])
    if(PlayAgain != 'y'):
        print(fstr(StringDictionary['GameResults'], locals()))
        print(StringDictionary['Goodbye'])
        PlayingGame = False
            
