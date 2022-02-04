import csv
import os
import time
import statistics
import ast

# ! Notes for RSPDprinter:
    # This file reads raw counts for names (in 50 separate files, one for each state) and a CSV file containing birth totals (a total for all F 1931 births in AL, all M 1931 births in AL, etc) and outputs a .txt file holding all the RSPD values for individual name-year-sex combinations.

    # A number of parameters are hard-coded: M or F, starting year, ending year, plain vs. rolling average.
    # The program loops through each year in a range from the starting to the ending year; for each year, it runs the "processDataUpToRSPD" function.
    # It writes a JSON-like .txt file with a filename like "RSPDsF_1931-2020.txt".



all50States = ['AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']
all_data = []    # this will hold all the data--except we'll restrict it the relevant year and gender--so we don't have to reread files
name_list = []   # this will hold all the relevant first names, each only ONCE
sortedNames = []   # this will hold all the relevant first names, each only ONCE, in order of declining frequency
sortedLimitedNames = []   # this will hold all the top 100 most frequent first names, sorted, each only ONCE
allBirthsList = {}
small_dictio = {}
by_name_dictio = {}
residualsDictio = {}
z_score_dictio = {}
red4 = []
red3 = []
red2 = []
red1 = []
blue1 = []
blue2 = []
blue3 = []
blue4 = []
neutral = []
grayNED = []

similsForOneName = {}       # this is for state similarity measurements
allSimils = {}              # this is for state similarity measurements
focalState = "none"         # this is for state similarity measurements
nonfocalState = "none"         # this is for state similarity measurements
colorGIMPstring = "none"         # this is for state similarity measurements
nameComparisonDictio = {}         # this is for testing which names are similar



# row[0] is state, e.g. "AK"
# row[1] is gender, e.g. "F"
# row[2] is year, e.g. "1973"
# row[3] is name, e.g. "Jeanette"
# row[4] is number of babies, e.g. "63"



def processDataUpToRSPD(year,sex):

    print("Analyzing raw numbers for " + sex + " in " + year + "...")

    currentFolder = os.scandir()

    all_data.clear()
    name_list.clear()
    small_dictio.clear()
    by_name_dictio.clear()
    global sortedNames
    global sortedLimitedNames


    yearBirthTotalsFile = open("count_all_revised.csv", "r")
    for line in yearBirthTotalsFile:
        if line.startswith(year+","+sex):
            #print(line[line.find("{"):])                # get the substring starting with the first {, continuing until the end
            allBirthsList = line.split(",")
            allBirthsList[51] = allBirthsList[51].strip("\n")
            # print(allBirthsList[51], len(allBirthsList[51]))
            # input()

    # The exact contents of an allBirthsList are written anew every year-loop, but they always refer to:
        # index     what
        # 0         year
        # 1         sex
        # 2         AL
        # 3         AK
        # 4         AZ
        # 5         AR
        # ...
        # 51        WY

    yearBirthTotalsFile.close()

    for entry in currentFolder:             # first, we need to make the list of names
        if entry.name.endswith('.TXT'):     # consider only the .txt files
            with open(entry.name) as csv_file:      # let's open that .txt file as a CSV file
                csv_reader = csv.reader(csv_file, delimiter=",")
                for row in csv_reader:          # take a row, and--
                    stateIndex = all50States.index(row[0]) + 2
                    if row[1] == sex and row[2] == year and not row[0] == "DC" and not allBirthsList[stateIndex] == "###":
                        row[4] = int(row[4])/int(allBirthsList[stateIndex])
                        all_data.append(row)
                        # print(all_data)
                        if row[3] not in name_list:          # if the name isn't in the list already...
                            name_list.append(row[3])             # add it to the end of the list

    # print("Name list:",name_list)
    # print("all_data:",all_data)
    # input()



    # We saved all the data, so we don't have to read from files again. We also have a list of all the names that appear in the relevant data. Now, we can make the actual dictionary...

    for firstName in name_list:      # go through all the names in the name list
        for row in all_data:         # keeping in mind one specific first name, go through all the rows in the "all_data" list
            if firstName == row[3]:     # if this given row has info on the current first name, then....
                small_dictio.setdefault(row[0],float(row[4]))   # inserts a key that's a state (e.g. 'MN') with a value that's the proportion of babies with that name (e.g. .000253478)
        if len(small_dictio) > 16:
            by_name_dictio[firstName] = small_dictio.copy()    # this puts the small dictionary--each states' data on ONE name--into the larger dictionary
        small_dictio.clear()

    # The section above builds 'by_name_dictio', a dictionary of dictionaries. The top level keys are names, whose values are dictionaries. These dictionaries have keys that are states, whose values are proportions of that name in the whole birth population. For example...
    # {'Jacob': {'AK': 0.014857, 'AL': 0.0152157...'Demarion': {'GA': 9.192e-05, 'IL': 0.0001588, 'MI': 0.00011025, 'TX': 6.0356e-05},...

    # Note that states will be missing from by_name_dictio if they had fewer than 5 births with the given name.

    # small_dictio, also used above, looks like:
        # {'AK': 0.014857, 'AL': 0.0152157...'WY': 0.0092873}


    for firstName in by_name_dictio.keys():

        # print(by_name_dictio[firstName].values())
        # input()

        mean = statistics.mean(by_name_dictio[firstName].values())
        pStDev = statistics.pstdev(by_name_dictio[firstName].values())

        # print("Here's a checkpoint.")
        # input()

        by_name_dictio[firstName]['mean'] = mean
        by_name_dictio[firstName]['pStDev'] = pStDev

    # Great, we've included the mean and the standard deviation (p-type). Now we need to create a dictionary for residuals.
    residualsDictio = by_name_dictio.copy()   # The .copy() method makes an independent copy--they're not linked
    for firstName in residualsDictio.keys():
        for state in residualsDictio[firstName].keys():
            residualsDictio[firstName][state] = by_name_dictio[firstName][state] - by_name_dictio[firstName]['mean']

    # And now we have a dictionary full of residuals, fantastic! Now we need a dictionary for "what percentage of a standard deviation each residual is".


    z_score_dictio = by_name_dictio.copy()
    namesDictionaryString = "'"+year+"'"
    namesDictionaryString = namesDictionaryString + ": {"
    for firstName in z_score_dictio.keys():
        statesDictionaryString = "'"+firstName+"'"
        statesDictionaryString = statesDictionaryString + ": {"
        for state in z_score_dictio[firstName].keys():
            if by_name_dictio[firstName]['pStDev'] != 0:
                if state != "mean" and state != "pStDev":
                    statesDictionaryString = statesDictionaryString + "'"+state+"': "+str(residualsDictio[firstName][state] / by_name_dictio[firstName]['pStDev'])+", "
        statesDictionaryString = statesDictionaryString.rstrip(" ,")
        statesDictionaryString = statesDictionaryString + "}, "
        namesDictionaryString = namesDictionaryString + statesDictionaryString
    namesDictionaryString = namesDictionaryString.rstrip(" ,") + "}"
    if int(year) != yearAfterEndingYear-1:
        namesDictionaryString = namesDictionaryString + ", "
    # fileToWrite.write(namesDictionaryString)



    return namesDictionaryString


############### END FUNCTION: processDataUpToRSPD DEFINITION ####################
############################################################
############################################################


userMF = "M"
startingYear = 1931             # reset to 1931
yearAfterEndingYear = 2021
plainOrRollingAverageSelection = 2

fileToWrite = open("RSPDs" + userMF + "_" + str(startingYear) + "-" + str(yearAfterEndingYear-1) + ".txt", "w")
oneNameDictio = {}
namesDictionaryStringMain = "{"

yearRange = range(startingYear,yearAfterEndingYear)        # the range generated will end with the year BEFORE the second number specified
for year in yearRange:
    year = str(year)
    try:
        namesDictionaryStringMain = namesDictionaryStringMain + processDataUpToRSPD(year,userMF)


    except:
        print("Something went wrong with the year " + year)
        input()

fileToWrite.write(namesDictionaryStringMain)
fileToWrite.write("}")


try:
    fileToWrite.close()
    currentFolder.close()
except:
    pass
