import os
import json
import gloomlog


def multipleChoiceQuestion(question, options, rangeOptions=None):
    """
    question (str):
        the question to the user
    options (tuple of strings):
        the options the question allows the user to choose from
    rangeOptions(str):
        overrides autogenerations of options shown in question

    Keeps asking the user until a valid option is inputted

    Returns the option from options chosen by the user (str)
    """
    assert type(question) == str
    assert type(options) == tuple
    for i in options:
        assert type(i) == str
    if rangeOptions is None:
        rangeOptions = str(options)
    else:
        assert type(rangeOptions) == str

    while True:
        userInput = input(question + " " + rangeOptions + ": ")
        if userInput in options:
            return userInput
        else:
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


if __name__ == "__main__":
    # 'translate' between multiple string and object representations of encounters
    nctrTransDict = {"S": {"class": gloomlog.Scenario, "titleName": "Scenario"},
                     "R": {"class": gloomlog.RoadEvent, "titleName": "Road Event"},
                     "C": {"class": gloomlog.CityEvent, "titleName": "City Event"}}

    listSaves = []

    for save in os.listdir("__gloomsave__"):
        if save.endswith(".json.gml"):
            listSaves.append(save.replace(".json.gml", ""))

    save = None
    ncrtUser = gloomlog.CityEvent(0)

    if len(listSaves) > 0:
        if yesNoQuestion("Would you like to load a save file?"):
            save = multipleChoiceQuestion(
                "Which save would you like to load?", tuple(listSaves))
            with open("__gloomsave__/" + save + ".json.gml", "r") as file:
                saveJSON = json.loads(file.read())
            lastNctr = saveJSON["EnounterList"][-1]

            try:
                # list(lastNctr.keys())[0] returns the encounter subclass as a string
                ncrtUser = nctrTransDict[list(lastNctr.keys())[0][0]]["class"](
                    fullJSON=json.dumps(lastNctr))
            except:
                print("Invalid save file :(")
                exit()

    print("Your last encounter was:")
    print(ncrtUser)

    if not yesNoQuestion("Would you like to set a new save?"):
        print("Bye!")
        exit()

    if save is None:
        save = input("How would you like to call your save file?: ")

    newEncounter = nctrTransDict[multipleChoiceQuestion(
        "What type was your last encounter?",
        tuple(nctrTransDict[i]["titleName"] for i in nctrTransDict.keys())
    )[0]]

    newEncounterInfo = []

    # get encounter number
    newEncounterInfo.append(
        int(multipleChoiceQuestion(
            "What is the number of the {encounter} you did?".format(
                encounter=newEncounter["titleName"].lower()),
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
        saveInfo = {"EnounterList": [json.loads(newEncounter.toJSON()), ]}
    except:
        print("Invalid encounters created :(")
        print("Please try again")
        exit()

    os.makedirs("__gloomsave__", exist_ok=True)

    with open("__gloomsave__/" + save + ".json.gml.new", "x") as file:
        file.write(json.dumps(saveInfo, indent=2))

    if os.path.exists("__gloomsave__/" + save + ".json.gml.prev"):
        os.rename("__gloomsave__/" + save + ".json.gml.prev",
                  "__gloomsave__/" + save + ".json.gml.old")

    if os.path.exists("__gloomsave__/" + save + ".json.gml"):
        os.rename("__gloomsave__/" + save + ".json.gml",
                  "__gloomsave__/" + save + ".json.gml.prev")

    if os.path.exists("__gloomsave__/" + save + ".json.gml.new"):
        os.rename("__gloomsave__/" + save + ".json.gml.new",
                  "__gloomsave__/" + save + ".json.gml")

    if os.path.exists("__gloomsave__/" + save + ".json.gml.old"):
        os.remove("__gloomsave__/" + save + ".json.gml.old")

    print("Saved:")
    print(newEncounter)
    print("Bye!")
