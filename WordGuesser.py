import random

def OpenDictionary():
    dictionary = {
        0: 'creamer',
        1: 'apples',
        2: 'pears',
        3: 'cough',
        4: 'salmon'
    }
    
    return dictionary

def SelectWord(dictionary):
    # Remove an arbitrary selection from the dictionary
    # Removing will ensure the word is not selected again
    randomKey = random.randint(0, len(dictionary))
    SelectedWord = str(dictionary.pop(randomKey))
    
    SelectedWord.lower()
    return SelectedWord

def InitDisplayList(Word):
    DisplayList = list()
    
    for char in Word:
        DisplayList.append(False)
    
    return DisplayList

def ShowWord(Word, DisplayList):
    # Create the Displayed version of the word with '_' whereever
    # DisplayList is False and the character from Word where
    # it is true
    DisplayWord = str()
    for index, char in enumerate(Word):
        if DisplayList[index]:
            DisplayWord += char
        else:
            DisplayWord += "_"
    
    # Show DisplayWord as a Clue
    print("Clue: %s (%d letters)" % (DisplayWord, len(DisplayWord)))
    

def CheckChar(Word, DisplayList, UserInput):
    # Go through all of the characters in the Word and turn on the display
    # for each that matches the User Input
    for index, char in enumerate(Word):
        if char == UserInput:
            DisplayList[index] = True


        

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

PlayingGame = True
while PlayingGame:
    Word = SelectWord(dictionary)

    DisplayList = InitDisplayList(Word)

    TurnCounter = 0
    GameMessage = "Sorry....Game Over. Better luck next time."
    SuccessMessage = "Congratulations!!!! You have successfully guessed the word"
    while TurnCounter < 7:
        ShowWord(Word, DisplayList)

        UserInput = GetUserInput()

        if(len(UserInput) == 1):
            # Check if character is in the word list
            CheckChar(Word, DisplayList, UserInput)
            # Need to check if all characters filled in the
            if(sum(DisplayList) == len(DisplayList)):
                GameMessage = SuccessMessage
                break
            TurnCounter += 1
        else:
            # Check if the guess is correct
            if UserInput == Word:
                GameMessage = SuccessMessage
                break
            
    print(GameMessage + "(%s rounds)" % (TurnCounter))
    PlayAgain = input("Would you like to play again? (y/n)")
    if(PlayAgain != 'y'):
        print("Goodbye")
        PlayingGame = False
            
