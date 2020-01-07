import os
import json
import gloomlog


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
    #, literal options + numbered positions
    @, literal options + one character shorthands
    >, literals + numbers + shorthands

    Returns the option from options chosen by the user (str)
    """

    assert type(question) == str
    assert type(options) == tuple
    assert len(options) > 0

    for i in options:
        assert type(i) == str

    # assert that options are unique
    dictOptions = {i: True for i in options}
    assert len(dictOptions) == len(options)

    if rangeOptions is None:
        if len(options) > 1:
            rangeOptions = str(options)
        else:
            rangeOptions = "(" + options[0] + ")"
    else:
        assert type(rangeOptions) == str

    # if first characters of options contain no digits, allow for numbered selection
    for i in options:
        if i[0].isdigit():
            containsDigits = True
            break
    else:
        containsDigits = False

    # if first characters in options are unique, allow for shorthand selection
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

    while True:
        userInput = input(question + " " + rangeOptions)
        if userInput in options:
            return userInput
        else:
            if userInput in fastDict:
                return fastDict[userInput]
            if not containsDigits:
                try:
                    userInput = int(userInput)
                    assert userInput > 0
                except:
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

    assert type(question) == str

    return multipleChoiceQuestion(question, ('yes', 'no')) == 'yes'


def writeNewTextFile(fileName, fileText):
    """
    fileName (str): path name of the file to write
    fileText (str): text to write in the file

    Write a new text file to disk.
    """

    assert type(fileName) == str
    assert type(fileText) == str

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

    assert type(saveFile) == str

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

    assert type(savePath) == str
    assert type(saveFile) == str
    assert type(saveInfo) == str

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


if __name__ == "__main__":
    # 'translate' between string and object representations of encounters
    nctrTransDict = {"Scenario": {"class": gloomlog.Scenario, "friendlyName": "Scenario"},
                     "RoadEvent": {"class": gloomlog.RoadEvent, "friendlyName": "Road Event"},
                     "CityEvent": {"class": gloomlog.CityEvent, "friendlyName": "City Event"}}

    # this value is also in .gitignore, change it together with this one
    savePath = "__gloomsave__"
    saveExtension = ".json.gml"

    listSaves = []

    if os.path.exists(savePath):
        for saveFile in os.listdir(savePath):
            if saveFile.endswith(saveExtension):
                listSaves.append(saveFile.replace(saveExtension, ""))

    saveFile = None
    ncrtUser = gloomlog.CityEvent(0)

    if len(listSaves) > 0:
        if yesNoQuestion("Would you like to load a save file?"):
            saveFile = multipleChoiceQuestion(
                "Which save would you like to load?", tuple(listSaves))
            with open(savePath + "/" + saveFile + saveExtension, "r") as file:
                saveJSON = json.loads(file.read())
            lastNctr = saveJSON["EnounterList"][-1]

            try:
                ncrtUser = nctrTransDict[lastNctr["type"]]["class"](
                    fullJSON=json.dumps(lastNctr))
            except:
                print("Invalid save file :(")
                exit()

    print("Your last encounter was:")
    print(ncrtUser)

    if not yesNoQuestion("Would you like to set a new save?"):
        print("Bye!")
        exit()

    if saveFile is None:
        saveFile = input(
            "How would you like to call your save file?: ").lower()
        if saveFile in listSaves:
            print('Save already exists.')
            print(
                'Please rerun the programm and load that save or save under a different name.')
            exit()

    newEncounter = nctrTransDict[multipleChoiceQuestion(
        "What type was your last encounter?",
        tuple(nctrTransDict[i]["friendlyName"] for i in nctrTransDict)
    ).replace(" ", "")]

    newEncounterInfo = []

    # get encounter number
    newEncounterInfo.append(
        int(multipleChoiceQuestion(
            "What is the number of the {encounter} you did?".format(
                encounter=newEncounter["friendlyName"].lower()),
            tuple(str(i) for i in range(1, 101)),
            "(1-100)")))

    if newEncounter["class"] == gloomlog.Scenario:
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

    newEncounter = newEncounter["class"](*newEncounterInfo)

    try:
        saveInfo = json.dumps({"EnounterList": [json.loads(newEncounter.toJSON()), ]},
                              indent=2)
    except:
        print("Invalid encounters created :(")
        print("Please try again")
        exit()

    saveToFile(savePath, saveFile + saveExtension, saveInfo)

    print("Saved:")
    print(newEncounter)
    print("Bye!")
