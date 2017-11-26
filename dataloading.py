import json
import csv
from pprint import pprint
import glob
import pickle
import sentence_tokenizer

datafiles = glob.glob("data/*.csv")

speech = {('',): {}}

with open('creds') as file:
    file = file.read().strip().split('\n')

name = file[2].lower()

for file in datafiles:
    f = open(file)

    spamreader = csv.reader(f, delimiter=',', quotechar='|')

    otherspeach = []
    karlspeech = False

    for row in spamreader:
        if not "Date" in row:
            row = [x.strip("\"") for x in row]
            message = tuple(row[3].split())
            lowered = tuple(sentence_tokenizer.sorting_pos(row[3].lower()))

            if name not in row[2].lower():
                if not lowered in speech:
                    speech[lowered] = {}

                if not karlspeech:
                    otherspeach.append(lowered)

                else:
                    otherspeach = [lowered]
                    karlspeech = False

            else:
                karlspeech = True
                if otherspeach:
                    for sentence in otherspeach:
                        if message in speech[sentence]:
                            speech[sentence][message] += 1
                        else:
                            speech[sentence][message] = 1

                else:
                    if message in speech[('',)]:
                        speech[('',)][message] += 1
                    else:
                        speech[('',)][message] = 1


print("Data loaded")
print(datafiles)

pickle.dump(speech, open('data/man.karl', 'wb'))


