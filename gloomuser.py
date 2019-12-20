import os
import json
import gloomlog


def multipleChoiceQuestion(question, options):
    """
    question (str):
        the question to the user
    options (iterable of strings):
        the options the question allows the user to choose from

    Keeps asking the user until a valid option is inputted

    Returns the option from options chosen by the user (str)
    """
    while True:
        userInput = input(question)
        if userInput in options:
            return userInput
        else:
            print("Invalid input")


if __name__ == "__main__":
    if os.path.exists("save.json.gml"):
        with open("save.json.gml", "r") as file:
            saveJSON = json.loads(file.read())
        lastNctrType = [*saveJSON["EnounterList"][-1]][0]
        lastNctrInfo = saveJSON["EnounterList"][-1][lastNctrType]

        if lastNctrType[0] == "S":
            ncrtUser = gloomlog.Scenario(scenarioJSON=json.dumps(lastNctrInfo))
        elif lastNctrType[0] == "R":
            ncrtUser = gloomlog.RoadEvent(eventJSON=json.dumps(lastNctrInfo))
        elif lastNctrType[0] == "C":
            ncrtUser = gloomlog.CityEvent(eventJSON=json.dumps(lastNctrInfo))
        else:
            print("Invalid save file :(")
            exit()
    else:
        ncrtUser = gloomlog.CityEvent(0)

    print("Your last encounter was:")
    print(ncrtUser)

    if multipleChoiceQuestion("Would you like to set a new save (y/n)?: ", ("y", "n")) == "n":
        print("Bye!")
        exit()

    newEncounter = multipleChoiceQuestion(
        "What type was your last encounter (Scenario/Road Event/City Event), (S/R/C)?: ", ("Scenario", "Road Event", "City Event", "S", "R", "C"))

    if newEncounter[0] == "S":
        newEncounter = "scenario"
    elif newEncounter[0] == "R":
        newEncounter = "road event"
        newEncounterClass = gloomlog.RoadEvent
    else:
        newEncounter = "city event"
        newEncounterClass = gloomlog.CityEvent

    newEncounterNumber = int(multipleChoiceQuestion(
        "What is the number of the {encounter} you did (1-100)?: ".format(encounter=newEncounter), [str(i) for i in range(1, 101)]))

    if newEncounter[0] == "s":
        newEncounterName = input("What is the name of the scenario you did?: ")
        newEncounterGridLocChar = multipleChoiceQuestion(
            "What is the character of that scenario's location (A-O)?: ", [chr(i) for i in range(65, 80)])
        newEncounterGridLocNumb = int(multipleChoiceQuestion(
            "What is the number of that scenario's location (1-18)?: ", [str(i) for i in range(1, 19)]))
        newEncounterGridLoc = gloomlog.GridLocation(
            newEncounterGridLocChar, newEncounterGridLocNumb)
        newEncounter = gloomlog.Scenario(
            newEncounterNumber, newEncounterName, newEncounterGridLoc)
    else:
        newEncounter = newEncounterClass(newEncounterNumber)

    nctrJSON = newEncounter.toJSON()
    nctrInfo = json.loads(nctrJSON)

    if type(newEncounter) == gloomlog.Scenario:
        saveInfo = {"EnounterList": [{"Scenario": nctrInfo}, ]}
    elif type(newEncounter) == gloomlog.RoadEvent:
        saveInfo = {"EnounterList": [{"RoadEvent": nctrInfo}, ]}
    elif type(newEncounter) == gloomlog.CityEvent:
        saveInfo = {"EnounterList": [{"CityEvent": nctrInfo}, ]}
    else:
        print("Invalid encounters created :(")
        print("Please try again")
        exit()

    with open("save_new.json.gml", "x") as file:
        file.write(json.dumps(saveInfo, indent=2))

    if os.path.exists("save_prev.json.gml"):
        os.rename("save_prev.json.gml", "save_old.json.gml")

    if os.path.exists("save.json.gml"):
        os.rename("save.json.gml", "save_prev.json.gml")

    if os.path.exists("save_new.json.gml"):
        os.rename("save_new.json.gml", "save.json.gml")

    if os.path.exists("save_old.json.gml"):
        os.remove("save_old.json.gml")

    print("Saved:")
    print(newEncounter)
    print("Bye!")
