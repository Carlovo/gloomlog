import os
import json
import gloomlog


def tupleToPrettyStr(aTuple):
    """

    """

    if len(aTuple) > 1:
        return str(aTuple)
    else:
        return "(" + aTuple[0] + ")"


# implement default question='' at some point
def multipleChoiceQuestion(question, options, rangeOptions=None):
    """
    question (str):
        the question to the user
    options (tuple of unique strings):
        the options the question allows the user to choose from
    rangeOptions(str):
        overrides autogenerations of options shown in question

    Keeps asking the user until a valid option is inputted.

    User can input a literal option.
    User can input the number of an option in options,
        if the first character of no option contains a number.
    User can input the first character of an option in options,
        if all first characters in options are unique.

    After the question comes a signal that the user may input:
    :, only literal options
    # , literal options + numbered positions
    @, literal options + one character shorthands
    >, literals + numbers + shorthands

    Returns the option from options chosen by the user (str)
    """

    assert isinstance(question, str)
    assert isinstance(options, tuple)
    assert options

    for i in options:
        assert isinstance(i, str)

    # assert that options are unique
    dictOptions = {i: True for i in options}
    assert len(dictOptions) == len(options)

    if rangeOptions is None:
        rangeOptions = tupleToPrettyStr(options)
    else:
        assert isinstance(rangeOptions, str)

    # if first characters of options contain no digits,
    # allow for numbered selection
    for i in options:
        if i[0].isdigit():
            containsDigits = True
            break
    else:
        containsDigits = False

    # if first characters in options are unique,
    # allow for shorthand selection
    fastDict = {i[0]: i for i in options}
    if len(fastDict) != len(options):
        fastDict = {}
        if containsDigits:
            rangeOptions += ": "
        else:
            rangeOptions += "# "
    else:
        if containsDigits:
            rangeOptions += "@ "
        else:
            rangeOptions += "> "

    if len(question) > 0:
        rangeOptions = ' ' + rangeOptions

    while True:
        userInput = input(question + rangeOptions)
        if userInput in options:
            return userInput
        else:
            if userInput in fastDict:
                return fastDict[userInput]
            if not containsDigits:
                try:
                    userInput = int(userInput)
                    assert userInput > 0
                except BaseException:
                    print("Invalid input")
                else:
                    userInput -= 1
                    if userInput < len(options):
                        return options[userInput]
                    else:
                        print("Inputted number out of option bounds")
            else:
                print("Invalid input")


def yesNoQuestion(question):
    """
    question (str):
        the question to the user

    Keeps asking the user until 'yes', 'no', '1' or '2' is inputted
    '1' = 'yes'
    '2' = 'no'

    Returns whether the user chose 'yes' (bool)
    """

    assert isinstance(question, str)

    return multipleChoiceQuestion(question, ('yes', 'no')) == 'yes'


def writeNewTextFile(fileName, fileText):
    """
    fileName (str): path name of the file to write
    fileText (str): text to write in the file

    Write a new text file to disk.
    """

    assert isinstance(fileName, str)
    assert isinstance(fileText, str)

    with open(fileName, "x") as file:
        file.write(fileText)


def _backupCreation_(saveFile):
    """
    This function should only be used by saveToFile.
    Use at your own risk.

    saveFile (str): file name of the save file

    Sets the current save file to become a backup file.
    Sets the new save file to become the current save file.
    """

    assert isinstance(saveFile, str)

    os.rename(saveFile, saveFile + ".prev")
    os.rename(saveFile + ".new", saveFile)


def saveToFile(savePath, saveFile, saveInfo):
    """
    savePath (str): relative path where to save the file
    saveFile (str): base name of the save file to write
    saveInfo (str): save info to write in the file

    Saves text to a file.
    Also, checks if a directory for saving and backups exist,
    creates a directory and rotates saves and backups if present.
    """

    assert isinstance(savePath, str)
    assert isinstance(saveFile, str)
    assert isinstance(saveInfo, str)

    saveFile = savePath + "/" + saveFile

    if os.path.exists(savePath):
        if os.path.exists(saveFile):
            writeNewTextFile(saveFile + ".new", saveInfo)
            if os.path.exists(saveFile + ".prev"):
                os.rename(saveFile + ".prev", saveFile + ".old")
                _backupCreation_(saveFile)
                os.remove(saveFile + ".old")
            else:
                _backupCreation_(saveFile)
            return
    else:
        os.mkdir(savePath)

    writeNewTextFile(saveFile, saveInfo)


def exitInterface():
    """
    Breaks are not allowwed outside of a loop :(
    Exceptions and generators would be overkill
    So use the flag 'stay' in every userOptionDict
    and this simple function instead
    """

    pass


def presentUserInterface(interfaceHeader, userOptionDict):
    """

    """

    interfaceTop = ''
    interfaceBottom = ''
    userOptionTuple = tuple(i for i in userOptionDict)

    maxLen = max(
        len(interfaceHeader),
        len(tupleToPrettyStr(userOptionTuple) + ":")
    )

    for _ in range(maxLen):
        interfaceTop += '='
        interfaceBottom += '-'

    while True:
        print('')
        print(interfaceTop)
        print(interfaceHeader)
        print(interfaceTop)

        for option in userOptionDict:
            print(userOptionDict[option]["print"])

        print(interfaceBottom)
        print('Please choose from')
        userInput = multipleChoiceQuestion('', userOptionTuple)
        try:
            assert userInput in userOptionDict
        except KeyError:
            errorExitGloomlog()
        print(interfaceBottom)

        userOptionDict[userInput]["function"](
            *userOptionDict[userInput]["args"])

        if not userOptionDict[userInput]["stay"]:
            break


def presentUserInterfaceMain(userOptionDictDefaults):
    """

    """

    # 'translate' between string and object representations of encounters
    # setting this thing all the way up here without using it
    # and then passing it all the way down where it is used, is wrong;
    # needs to be refactored
    nctrTransDict = {
        "Scenario": {
            "class": gloomlog.Scenario, "friendlyName": "scenario"},
        "RoadEvent": {
            "class": gloomlog.RoadEvent, "friendlyName": "road event"},
        "CityEvent": {
            "class": gloomlog.CityEvent, "friendlyName": "city event"}}

    # this value is also in .gitignore, change it together with this one
    # this stuff should be refactored into some DAL like abstraction at some point
    savePath = "__gloomsave__"
    saveExtension = ".json.gml"

    listSaves = []
    # implement reloading on new save file creation, or something
    if os.path.exists(savePath):
        for saveFile in os.listdir(savePath):
            if saveFile.endswith(saveExtension):
                listSaves.append(saveFile.replace(saveExtension, ""))

    userOptionDictMain = userOptionDictDefaults.copy()
    userOptionDictMain["new"] = {
        "function": newCampaignSave,
        "args": [savePath, listSaves, saveExtension, userOptionDictDefaults, nctrTransDict],
        "stay": True,
        "print": "Create NEW campaign save file"
    }
    if listSaves:
        userOptionDictMain["load"] = {
            "function": loadCampaignSave,
            "args": [listSaves, savePath, saveExtension, nctrTransDict, userOptionDictDefaults],
            "stay": True,
            "print": "LOAD a campaign save file"}
        # implement delete, copy and restore here at some point

    presentUserInterface('What would you like to do?', userOptionDictMain)


def newCampaignSave(savePath, listSaves, saveExtension, userOptionDictDefaults, nctrTransDict):
    """
    listSaves (list of str): list of save files already present


    """

    if listSaves:
        print("The following campaign save names are already taken:")
        print(tuple(i for i in listSaves))

    while True:
        print("Campaign save names will be converted to lower case.")
        saveFile = input(
            "How would you like to call your campaign save file?: ").lower()
        if saveFile in listSaves:
            print('Save already exists.')
        else:
            break

    if yesNoQuestion(
            'Would you like to add the default campaign starter to your save (recommended)?'):
        presentUserInterfaceSave(savePath, saveFile + saveExtension, userOptionDictDefaults, [
                                 gloomlog.CityEvent(0), ], nctrTransDict)
    else:
        # refactor presentUserInterfaceSave to optional encounter list
        presentUserInterfaceSave(
            savePath, saveFile + saveExtension, userOptionDictDefaults, [], nctrTransDict)


def loadCampaignSave(listSaves, savePath, saveExtension, nctrTransDict, userOptionDictDefaults):
    """
    listSaves (list of str): list of save files already present
    """

    saveFile = multipleChoiceQuestion(
        "Which save would you like to load?", tuple(listSaves))
    with open(savePath + "/" + saveFile + saveExtension, "r") as file:
        saveDict = json.loads(file.read())

    try:
        encounterListPython = saveDict["EnounterList"]
        encounterListGloomlog = [nctrTransDict[i["type"]]["class"](
            fullJSON=json.dumps(i)) for i in encounterListPython]
    except BaseException:
        print("Invalid save file :(")
        errorExitGloomlog()

    presentUserInterfaceSave(savePath, saveFile + saveExtension,
                             userOptionDictDefaults, encounterListGloomlog, nctrTransDict)


def presentUserInterfaceSave(savePath, saveFileName, userOptionDictDefaults, encounterList, nctrTransDict):
    """

    """

    if encounterList:
        print("Your last encounter was:")
        print(encounterList[-1])
    else:
        print("Your campaign save does not yet contain any encounters.")

    userOptionDictSave = userOptionDictDefaults.copy()
    userOptionDictSave["add"] = {
        "function": addEncounterToSave,
        "args": [savePath, saveFileName, nctrTransDict],
        "stay": False,
        "print": "ADD new encounter (implemented as replace for now)"
    }
    userOptionDictSave["close"] = {
        "function": exitInterface,
        "args": [],
        "stay": False,
        "print": "CLOSE save and go back to main interface"
    }

    # implement here at some point:
    # SAVE progress
    # REMOVE encounters from save file
    # EDIT encounter properties
    # DELETE this save
    # Inspect BACKUP save file -> Maybe advanced interface
    # Try to FIX broken save file -> Maybe advanced interface

    presentUserInterface(
        'What would you like to do with the campaign save?',
        userOptionDictSave
    )


def addEncounterToSave(savePath, saveFileName, nctrTransDict):
    """
    pass for now
    """

    newEncounterFriendlyName = multipleChoiceQuestion(
        "What type was your last encounter?",
        tuple(nctrTransDict[i]["friendlyName"] for i in nctrTransDict)
    )

    for nctr in nctrTransDict:
        if nctrTransDict[nctr]["friendlyName"] == newEncounterFriendlyName:
            newEncounterClass = nctrTransDict[nctr]["class"]
            break
    else:
        print("Undefined class obtained")
        errorExitGloomlog()

    # newEncounter = nctrTransDict[multipleChoiceQuestion(
    #     "What type was your last encounter?",
    #     tuple(nctrTransDict[i]["friendlyName"] for i in nctrTransDict)
    # ).replace(" ", "")]

    newEncounterInfo = []

    # get encounter number
    newEncounterInfo.append(
        int(multipleChoiceQuestion(
            "What is the number of the {encounter} you did?".format(
                encounter=newEncounterFriendlyName),
            tuple(str(i) for i in range(1, 101)),
            "(1-100)")))

    if newEncounterClass == gloomlog.Scenario:
        # get scenario name
        newEncounterInfo.append(
            input("What is the name of the scenario you did?: "))
        # get/create scenario gridLocation
        newEncounterInfo.append(
            gloomlog.GridLocation(
                multipleChoiceQuestion(
                    "What is the character of that scenario's location?",
                    tuple(chr(i) for i in range(65, 80)), "(A-O)"),
                int(multipleChoiceQuestion(
                    "What is the number of that scenario's location?",
                    tuple(str(i) for i in range(1, 19)), "(1-18)"))
            ))

    newEncounter = newEncounterClass(*newEncounterInfo)

    try:
        saveInfo = json.dumps(
            {"EnounterList": [json.loads(newEncounter.toJSON()), ]}, indent=2)
    except BaseException:
        print("Invalid encounters created :(")
        errorExitGloomlog()

    saveToFile(savePath, saveFileName, saveInfo)

    print("Saved:")
    print(newEncounter)


def printHelp():
    """
    Print GloomLog's help text
    """

    print(':, only literal options')
    print('#, literal options + numbered positions')
    print('@, literal options + one character shorthands')
    print('>, literals + numbers + shorthands')


def exitGloomlog():
    """
    Gracefully exits GloomLog
    """

    print('Bye!')
    exit()


def errorExitGloomlog():
    """
    Something really strange happened...
    """

    print('Sorry, an unexpected error occured')
    print('GloomLog has to shut down :(')
    exit()


if __name__ == "__main__":
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    print('            Welcome to GloomLog              ')
    print('   An app for logging Gloomhaven campaigns   ')
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

    # 'translate' between string and function call
    userOptionDictDefaults = {
        "help": {
            "function": printHelp,
            "args": [],
            "stay": True,
            "print": "Show HELP"},
        "exit": {
            "function": exitGloomlog,
            "args": [],
            "stay": False,
            "print": "EXIT GloomLog"}
    }

    presentUserInterfaceMain(userOptionDictDefaults)
