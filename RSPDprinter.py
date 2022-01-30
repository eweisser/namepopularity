import csv
import os
import time
import statistics
import ast

# ! Notes for RSPDprinter:



all50States = ['AK','AL','AR','AZ','CA','CO','CT','DE','FL','GA','HI','IA','ID','IL','IN','KS','KY','LA','MA','MD','ME','MI','MN','MO','MS','MT','NC','ND','NE','NH','NJ','NM','NV','NY','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VA','VT','WA','WI','WV','WY']
allData = []    # this will hold all the data--except we'll restrict it the relevant year and gender--so we don't have to reread files
nameList = []   # this will hold all the relevant first names, each only ONCE
sortedNames = []   # this will hold all the relevant first names, each only ONCE, in order of declining frequency
sortedLimitedNames = []   # this will hold all the top 100 most frequent first names, sorted, each only ONCE
allBirthsDictio = {}
smallDictio = {}
byNameDictio = {}
residualsDictio = {}
resStDevPercDictio = {}
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
simpleCount = {}
printingDictio = {'AL':'pdb.gimp_drawable_edit_bucket_fill(map,0,533,333)\n','AK':'pdb.gimp_drawable_edit_bucket_fill(map,0,90,400)\npdb.gimp_drawable_edit_bucket_fill(map,0,165,430)\npdb.gimp_drawable_edit_bucket_fill(map,0,90,462)\npdb.gimp_drawable_edit_bucket_fill(map,0,38,439)\npdb.gimp_drawable_edit_bucket_fill(map,0,186,453)\npdb.gimp_drawable_edit_bucket_fill(map,0,44,484)\npdb.gimp_drawable_edit_bucket_fill(map,0,31,491)\npdb.gimp_drawable_edit_bucket_fill(map,0,167,440)\npdb.gimp_drawable_edit_bucket_fill(map,0,173,438)\npdb.gimp_drawable_edit_bucket_fill(map,0,27,411)\npdb.gimp_drawable_edit_bucket_fill(map,0,173,446)\npdb.gimp_drawable_edit_bucket_fill(map,0,180,444)\npdb.gimp_drawable_edit_bucket_fill(map,0,184,445)\n','AR':'pdb.gimp_drawable_edit_bucket_fill(map,0,450,300)\n','AZ':'pdb.gimp_drawable_edit_bucket_fill(map,0,160,300)\n','CA':'pdb.gimp_drawable_edit_bucket_fill(map,0,60,240)\n','CO':'pdb.gimp_drawable_edit_bucket_fill(map,0,260,230)\n','CT':'pdb.gimp_drawable_edit_bucket_fill(map,0,700,140)\n','DE':'pdb.gimp_drawable_edit_bucket_fill(map,0,677,200)\n','FL':'pdb.gimp_drawable_edit_bucket_fill(map,0,610,380)\n','GA':'pdb.gimp_drawable_edit_bucket_fill(map,0,585,330)\n','HI':'pdb.gimp_drawable_edit_bucket_fill(map,0,268,456)\npdb.gimp_drawable_edit_bucket_fill(map,0,249,429)\npdb.gimp_drawable_edit_bucket_fill(map,0,212,412)\npdb.gimp_drawable_edit_bucket_fill(map,0,177,398)\npdb.gimp_drawable_edit_bucket_fill(map,0,236,421)\npdb.gimp_drawable_edit_bucket_fill(map,0,236,428)\n','ID':'pdb.gimp_drawable_edit_bucket_fill(map,0,150,120)\n','IL':'pdb.gimp_drawable_edit_bucket_fill(map,0,480,200)\n','IN':'pdb.gimp_drawable_edit_bucket_fill(map,0,530,200)\n','IA':'pdb.gimp_drawable_edit_bucket_fill(map,0,420,170)\n','KS':'pdb.gimp_drawable_edit_bucket_fill(map,0,360,240)\n','KY':'pdb.gimp_drawable_edit_bucket_fill(map,0,550,240)\n','LA':'pdb.gimp_drawable_edit_bucket_fill(map,0,450,380)\n','ME':'pdb.gimp_drawable_edit_bucket_fill(map,0,730,60)\n','MD':'pdb.gimp_drawable_edit_bucket_fill(map,0,653,193)\npdb.gimp_drawable_edit_bucket_fill(map,0,622,195)\npdb.gimp_drawable_edit_bucket_fill(map,0,631,192)\n','MA':'pdb.gimp_drawable_edit_bucket_fill(map,0,708,124)\n','MI':'pdb.gimp_drawable_edit_bucket_fill(map,0,540,150)\npdb.gimp_drawable_edit_bucket_fill(map,0,490,90)\n','MN':'pdb.gimp_drawable_edit_bucket_fill(map,0,410,100)\n','MS':'pdb.gimp_drawable_edit_bucket_fill(map,0,490,340)\n','MO':'pdb.gimp_drawable_edit_bucket_fill(map,0,450,240)\n','MT':'pdb.gimp_drawable_edit_bucket_fill(map,0,230,80)\n','NE':'pdb.gimp_drawable_edit_bucket_fill(map,0,350,190)\n','NV':'pdb.gimp_drawable_edit_bucket_fill(map,0,100,200)\n','NH':'pdb.gimp_drawable_edit_bucket_fill(map,0,705,100)\n','NJ':'pdb.gimp_drawable_edit_bucket_fill(map,0,680,160)\n','NM':'pdb.gimp_drawable_edit_bucket_fill(map,0,250,310)\n','NY':'pdb.gimp_drawable_edit_bucket_fill(map,0,666,127)\npdb.gimp_drawable_edit_bucket_fill(map,0,694,157)\n','NC':'pdb.gimp_drawable_edit_bucket_fill(map,0,640,270)\n','ND':'pdb.gimp_drawable_edit_bucket_fill(map,0,340,80)\n','OH':'pdb.gimp_drawable_edit_bucket_fill(map,0,570,190)\n','OK':'pdb.gimp_drawable_edit_bucket_fill(map,0,380,290)\n','OR':'pdb.gimp_drawable_edit_bucket_fill(map,0,80,100)\n','PA':'pdb.gimp_drawable_edit_bucket_fill(map,0,640,170)\n','RI':'pdb.gimp_drawable_edit_bucket_fill(map,0,714,133)\n','SC':'pdb.gimp_drawable_edit_bucket_fill(map,0,620,300)\n','SD':'pdb.gimp_drawable_edit_bucket_fill(map,0,340,130)\n','TN':'pdb.gimp_drawable_edit_bucket_fill(map,0,530,280)\n','TX':'pdb.gimp_drawable_edit_bucket_fill(map,0,360,360)\n','UT':'pdb.gimp_drawable_edit_bucket_fill(map,0,180,210)\n','VT':'pdb.gimp_drawable_edit_bucket_fill(map,0,690,90)\n','VA':'pdb.gimp_drawable_edit_bucket_fill(map,0,640,230)\npdb.gimp_drawable_edit_bucket_fill(map,0,677,220)\n','WA':'pdb.gimp_drawable_edit_bucket_fill(map,0,100,40)\n','WV':'pdb.gimp_drawable_edit_bucket_fill(map,0,600,220)\n','WI':'pdb.gimp_drawable_edit_bucket_fill(map,0,470,120)\n','WY':'pdb.gimp_drawable_edit_bucket_fill(map,0,240,150)\n'}
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

    simpleCount.clear()
    allData.clear()
    nameList.clear()
    smallDictio.clear()
    byNameDictio.clear()
    global sortedNames
    global sortedLimitedNames


    yearBirthTotalsFile = open("countAll.txt", "r")
    for line in yearBirthTotalsFile:
        #print(line)
        if line.startswith(sex+year):
            #print(line[line.find("{"):])                # get the substring starting with the first {, continuing until the end
            allBirthsDictio = ast.literal_eval(line[line.find("{"):])

    yearBirthTotalsFile.close()
    #print(allBirthsDictio)

    for entry in currentFolder:             # first, we need to make the list of names
        if entry.name.endswith('.TXT'):     # consider only the .txt files
            with open(entry.name) as csv_file:      # let's open that .txt file as a CSV file
                csv_reader = csv.reader(csv_file, delimiter=",")
                for row in csv_reader:          # take a row, and--
                    if row[1] == sex and row[2] == year:
                        rawNum = row[4]                     # save the actual number of records as 'rawNum'
                        simpleCount.setdefault(row[3],0)    # put that into the simpleCount dictionary
                        simpleCount[row[3]] = simpleCount[row[3]] + int(rawNum) # update the simpleCount dictionary
                    if row[1] == sex and row[2] == year and not row[0] == "DC" and not (year == '1940' and row[0] == 'AK'):
                        row[4] = int(row[4])/allBirthsDictio[row[0]]   # turn the raw number into the percentage of babies with that name
                        allData.append(row)
                        if row[3] not in nameList:          # if the name isn't in the list already...
                            nameList.append(row[3])             # add it to the end of the list

    sortedNames = sorted(simpleCount,key=simpleCount.get,reverse=True)
    sortedLimitedNames = sortedNames[0:100]


    # We saved all the data, so we don't have to read from files again. We also have a list of all the names that appear in the relevant data. Now, we can make the actual dictionary...

    for firstName in nameList:      # go through all the names in the name list
        for row in allData:         # keeping in mind one specific first name, go through all the rows in the "allData" list
            if firstName == row[3]:     # if this given row has info on the current first name, then....
                smallDictio.setdefault(row[0],row[4])   # inserts a key that's a state (e.g. 'MN') with a value that's the proportion of babies with that name (e.g. .000253478)
        byNameDictio[firstName] = smallDictio.copy()    # this puts the small dictionary--each states' data on ONE name--into the larger dictionary
        smallDictio.clear()

    #The section above builds 'byNameDictio', a dictionary of dictionaries. The top level keys are names, whose values are dictionaries. These dictionaries have keys that are states, whose values are proportions of that name in the whole birth population. For example...
    #{'Jacob': {'AK': 0.014857, 'AL': 0.0152157...'Demarion': {'GA': 9.192e-05, 'IL': 0.0001588, 'MI': 0.00011025, 'TX': 6.0356e-05},...


    # Note that states will be missing from byNameDictio if they had fewer than 5 births with the given name.



    for firstName in byNameDictio.keys():
        mean = statistics.mean(byNameDictio[firstName].values())
        pStDev = statistics.pstdev(byNameDictio[firstName].values())

        byNameDictio[firstName]['mean'] = mean
        byNameDictio[firstName]['pStDev'] = pStDev

    #Great, we've included the mean and the standard deviation (p-type). Now we need to create a dictionary for residuals.
    residualsDictio = byNameDictio.copy()   # The .copy() method makes an independent copy--they're not linked
    for firstName in residualsDictio.keys():
        for state in residualsDictio[firstName].keys():
            residualsDictio[firstName][state] = byNameDictio[firstName][state] - byNameDictio[firstName]['mean']

    #And now we have a dictionary full of residuals, fantastic! Now we need a dictionary for "what percentage of a standard deviation each residual is".


    resStDevPercDictio = byNameDictio.copy()
    namesDictionaryString = "'"+year+"'"
    namesDictionaryString = namesDictionaryString + ": {"
    for firstName in resStDevPercDictio.keys():
        statesDictionaryString = "'"+firstName+"'"
        statesDictionaryString = statesDictionaryString + ": {"
        for state in resStDevPercDictio[firstName].keys():
            if byNameDictio[firstName]['pStDev'] != 0:
                if state != "mean" and state != "pStDev":
                    statesDictionaryString = statesDictionaryString + "'"+state+"': "+str(residualsDictio[firstName][state] / byNameDictio[firstName]['pStDev'])+", "
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





nameToMap = input('Choose a name: ')
userMF = input('Choose male or female (M/F): ')
print()
plainOrRollingAverageSelection = 2
# frameTime = input('How many milliseconds do you want each frame of the GIF to last? The default is 500. ')


#yearRange = range(1931,2020)
startingYear = 1931
yearAfterEndingYear = 2021      # reset to 2018

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

fileToWrite.write(namesDictionaryStringMain)
fileToWrite.write("}")
#print(oneNameDictio)


# end of gimpCode, only needs to be written once--at the end the file:
    # delete the original blank layer
# fileToWrite.write('img.remove_layer(orig)\n')
#     # this converts the image to an indexed color scheme, necessary for gifs
# fileToWrite.write('pdb.gimp_image_convert_indexed(img, 0, 0, 15, FALSE, TRUE, "ignored")\n')    # let's give it 15 colors--11 is the minimum
#     # this actually exports to a gif; there seem to be some problems with the 'save2' command
# fileToWrite.write('pdb.file_gif_save(img, None, \'C:\\Users\\Eric\\progs/names\\gimpCode\\Diachronic\\'+nameToMap+'_diachronic.gif\', \'C:\\Users\\Eric\\Progs/names\\gimpCode\\Diachronic\\'+nameToMap+'_diachronic.gif\', 0, 1, '+frameTime+', 2)\n')
# fileToWrite.write('pdb.file_gif_save2(img, None, \'C:\\Users\\Eric\\Progs\\names\\gimpCode\\Diachronic\\'+nameToMap+'_diachronic.gif\', \'C:\\Users\\Eric\\Progs\\names\\gimpCode\\Diachronic\\'+nameToMap+'_diachronic.gif\', 0, 1, 200, 2, 1, 1, 1)\n')


try:
    fileToWrite.close()
    currentFolder.close()
except:
    pass
