# dataprocessing.py

import glob
import json
import random
import pickle

responseDict = pickle.load(open('data/man.karl','rb'))
userInput = ("zehan",)

def findResponse(responseDict, userInput):
    outputs = {}
    matchMax = 0

    for key in responseDict.keys():
        matches = (1+len(set(key) & set(userInput)))/(1+len(set(key) | set(userInput)))
        if matches > matchMax:
            outputs = responseDict[key]
            matchMax = matches

        elif matches == matchMax:
            for key2 in responseDict[key].keys():
                if key2 in outputs:
                    outputs[key2] += responseDict[key][key2]
                else:
                    outputs[key2] = responseDict[key][key2]


    # Gets the number of responses to an input
    responseCount = 0
    for key in outputs.keys():
        responseCount += outputs[key]

    randomResponseNum = random.randint(0, responseCount - 1)

    numCounter = 0
    response = ""
    for key in outputs.keys():
        numCounter += outputs[key]
        if randomResponseNum < numCounter:
            response = key
            break

    # Response is the randomly generated response from the ai

    return response
