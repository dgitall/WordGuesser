import random
from urllib.request import urlopen

## Open a file from a github repository containing a bunch of words
## Load this into our internal dictionary
def OpenDictionary():
    dictionary = dict()
    print("Loading dictionary...")
   
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
    # Show DisplayWord as a Clue
    print("Clue: %s (%d letters remaining)" %
          (joined_string, len(DisplayList)-sum(DisplayList)))
    
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
    Message = "Enter a letter or guess the word: "
    
    while GetInput:
        # Prompt User Entry
        Entry = input(Message)
        # Is entry length > 0
        if len(Entry) <= 0:
            Message = "Enter a letter or guess the word: "
        else:
            # Is entry a string?
            if Entry.isnumeric():
                Message = "Only Characters...Try Again. Enter a letter or guess the word: "
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
    WinCount = 0
    GameCount += 1
    GameMessage = "Sorry....Game Over. Better luck next time."
    SuccessMessage = "Congratulations!!!! You have successfully guessed the word"
    ## Give the player 7 tries to guess the word. 
    while TurnCounter < 7:
        ## Display the clue
        print("Round: %s" % (TurnCounter + 1))
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
            
    print(GameMessage + " The word was: %s (%s/%s correct words)" % 
          (Word, sum(DisplayList), len(DisplayList)))
    PlayAgain = input("Would you like to play again? (y/n)")
    if(PlayAgain != 'y'):
        print("You won %s out of %s games" % (WinCount, GameCount))
        print("Goodbye")
        PlayingGame = False
            
