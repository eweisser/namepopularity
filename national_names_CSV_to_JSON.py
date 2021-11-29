import csv
import json

jsonDict = {}
top_names_json = []

currentYear = 1931
recordID = 1
while currentYear < 2021:
    with open("national_names/yob" + str(currentYear) + ".txt") as csv_file:
        recordM = {}
        recordF = {}
        csv_reader = csv.reader(csv_file, delimiter=",")
        recordM["id"] = recordID
        recordID = recordID + 1
        recordF["id"] = recordID
        recordID = recordID + 1
        recordM["year"] = currentYear
        recordM["sex"] = "M"
        recordF["year"] = currentYear
        recordF["sex"] = "F"
        recordM["fnames"] = ""
        recordF["fnames"] = ""
        rankNumberM = 1
        rankNumberF = 1
        for row in csv_reader:
            if row[1] == "M" and rankNumberM <= 100:
                recordM["fnames"] = recordM["fnames"] + row[0] + "&"
                # print(rankNumber, keyString, row[0])
                rankNumberM = rankNumberM + 1
            if row[1] == "F" and rankNumberF <= 100:
                recordF["fnames"] = recordF["fnames"] + row[0] + "&"
                rankNumberF = rankNumberF + 1
        # print(recordM)
        # print(recordF)
        top_names_json.append(recordM)
        top_names_json.append(recordF)
        # print(top_names_json)
    currentYear = currentYear + 1

jsonDict["records"] = top_names_json
print(jsonDict)

f = open("top_names_json.json", "x")
f.write(json.dumps(jsonDict))
f.close()
