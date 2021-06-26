import csv
import os
import time
import statistics
import ast

# ! Notes for gimpUniversal:
# This program begins by asking the user for a year and a gender. It builds an RSPD from scratch for that year-gender combination, from the countAll file and the individual state files.
# A quick summary:
#           operation no.       names       years       .txt output?    .csv output?        what's compared
#           1                   many        1           no              no                  names
#           2                   1 (spec)    1           yes             no                  states
#           3                   100         1           yes             no                  states*
#           4                   0           1           no              yes                 state-state pairs
#           5
#           6

# 1. Given a state, print out a list (in console) of the % of standard deviation for each of the boys' names that show up in that state in 2000. The list is sorted, highest values first. For example:
        # state HI percentages of standard deviation [for 2017]
        # Duke 4.6377...
        # Kai 4.4206...
        # Samson 4.4136...
        # ...
        # Samuel -3.1579

# 2. Given a name, create a .txt output file containing GIMP code that will create a US state-level popularity map for that name in the specified year when pasted into GIMP's Python-fu console. A summary of the relative popularity among states for that name will be printed to the console. For example:
        # 1.75+ SDs from mean: ['CA', 'NM']
        # 1.25 to 1.75 SDs from mean: ['DE']
        # ...
        # -1.75- SDs from mean: ['ID']
        # States with no data: ['RI','VT','WY']

    # The GIMP code will look like:
        # img = gimp.image_list()[0]
        # orig = pdb.gimp_image_get_layer_by_name(img,'blank')
        # map = pdb.gimp_layer_copy(orig,FALSE)
        # pdb.gimp_image_insert_layer(img,map,None,0)
        # pdb.gimp_item_set_name(map,'David')

    # issues:
        # not updated with latest GIMP map features
        # crashes if the name isn't common enough
        # output file not ready until program closes

# 3. create a .txt output file containing GIMP code that will create 100 US state-level popularity maps for each of the 100 most popular names (of the specified gender) in the specified year when pasted into GIMP's Python-fu console. A summary of the relative popularity among states for that name will be printed to the console.
    # The GIMP code will look like:
        # img = gimp.image_list()[0]
        # orig = pdb.gimp_image_get_layer_by_name(img,'blank')
        # map = pdb.gimp_layer_copy(orig,FALSE)
        # pdb.gimp_image_insert_layer(img,map,None,0)
        # pdb.gimp_item_set_name(map,'David')

    # issues:
        # not updated with latest GIMP map features


# 4. create a CSV file with the average difference between each combination of two states together, for one year. For example, it holds a value of .6104 for KY-MO; across the top 100 names for one sex, the average difference of % of standard deviation of popularity between KY and MO is .6104.

# let's do GIMP code for making maps comparing states to a central user-specified state
# let's measure names with popularity patterns like other names




# Also don't forget to change:
    # "F" / "M" flag in row[1] == "M" (appears twice)
    # year in row[2] == "####" (appears twice)
    # output .txt file name, year and sex


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
green1 = []
green2 = []
green3 = []
green4 = []
green5 = []
green6 = []
green7 = []
green8 = []
green9 = []
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

userYear = input('Choose a year: ')
userMF = input('Choose male or female (M/F): ')



def processDataUpToRSPD(year,sex):          # RSPD stands for residual standard deviation percent dictionary
                                            # Maybe it should be RPSD or DRPS. Oh well.

    print("Analyzing raw numbers for " + sex + " in " + year + "...\n")

    currentFolder = os.scandir()

    simpleCount.clear()
    allData.clear()
    nameList.clear()
    smallDictio.clear()
    byNameDictio.clear()
    global sortedNames
    global sortedLimitedNames
    global allBirthsDictio


    yearBirthTotalsFile = open("countAll.txt", "r")
    for line in yearBirthTotalsFile:
        #print(line)
        if line.startswith(sex+year):
            #print(line[line.find("{"):])                # get the substring starting with the first {, continuing until the end
            allBirthsDictio = ast.literal_eval(line[line.find("{"):])

    yearBirthTotalsFile.close()

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

    # Great, we've included the mean and the standard deviation (p-type). Now we need to create a dictionary for residuals.
    residualsDictio = byNameDictio.copy()   # The .copy() method makes an independent copy--they're not linked
    for firstName in residualsDictio.keys():
        for state in residualsDictio[firstName].keys():
            residualsDictio[firstName][state] = byNameDictio[firstName][state] - byNameDictio[firstName]['mean']

    # And now we have a dictionary full of residuals, fantastic! Now we need a dictionary for "what percentage of a standard deviation each residual is".

    resStDevPercDictio = byNameDictio.copy()
    for firstName in resStDevPercDictio.keys():
        for state in resStDevPercDictio[firstName].keys():
            if byNameDictio[firstName]['pStDev'] != 0:
                resStDevPercDictio[firstName][state] = residualsDictio[firstName][state] / byNameDictio[firstName]['pStDev']
        resStDevPercDictio[firstName].pop('mean')
        resStDevPercDictio[firstName].pop('pStDev')

    # for key in resStDevPercDictio.keys():
        #print(key)

    return resStDevPercDictio


############### END FUNCTION DEFINITION ####################
############################################################
############################################################


resStDevPercDictio = processDataUpToRSPD(userYear,userMF)






# Excellent. That's the main task. Now we can sort them a little.

while True:

    print('Choose an operation.\n \
    To see an individual state\'s report on names in a given year, enter a command like "state PA".\n \
    To output code that can be used in GIMP to make a map representing relative popularity for a specific name, just type the name itself.\n \
    To output code for maps like that for all of the top 100 names in the active year, type "top100".\n \
    To compare states as a whole (within a single year), enter "compare states".\n \
    To make code for a map showing states\' similarity to a specified state, enter "compare states to [PA]".\n \
    To see what names are similar to a specific name, enter "compare names to [Jessica]".')
    userInput = input('>>> ')
    print()


    if len(userInput) < 1 or userInput == "x" or userInput == "q" or userInput == "exit":
        break

    ################# NAMES' PROMINENCE FOR ONE STATE, DATA PRINTOUT ###############################

    # [operation 1]

    elif userInput.startswith('state '):
        residualsPercForOneState = {}
        for firstName in resStDevPercDictio.keys():
            for state in resStDevPercDictio[firstName].keys():
                if userInput.strip().endswith(state):
                    residualsPercForOneState[firstName] = resStDevPercDictio[firstName][state]
        print('*************', userInput, 'percentages of standard deviation')
        sortedResidualsPercForOneState = sorted(residualsPercForOneState,key=residualsPercForOneState.get,reverse=True)
        for item in sortedResidualsPercForOneState:
            print(item, residualsPercForOneState[item])

    ################# COMPARE ALL STATES DATA PRINTOUT TO FILE ###############################

    # [operation 4]

    elif userInput.startswith('compare states'):    # compare all states to each other

        for firstName in sortedLimitedNames:    # for every name in the top 100, sorted by rank...
            similsForOneName.clear()            # clear this dictionary
            #if len(resStDevPercDictio[firstName]) < 50:                # this just shows which states don't go to 50
                #print(firstName, len(resStDevPercDictio[firstName]))
            for state in resStDevPercDictio[firstName].keys():     # for each state
                for state2 in resStDevPercDictio[firstName].keys(): # for each combo of a state with another
                    if state < state2:
                        similsForOneName[state+state2] = abs(resStDevPercDictio[firstName][state] - resStDevPercDictio[firstName][state2])
            allSimils[firstName] = similsForOneName.copy()

        comboSum = 0
        comboCount = 0
        comboAverage = 0

        with open('similaritysortedTest.csv', mode='w', newline='') as simSortedFile:
            sortedWriter = csv.writer(simSortedFile)
            for state in all50States:     # for each state...
                #print('Starting with ' + state)
                #time.sleep(1)
                for state2 in all50States:     # for each state...
                    if state < state2:
                        #print('...and ' + state2)
                        #time.sleep(0.1)
                        for firstName in sortedLimitedNames:    # for each name in the top 100 names...
                            try:
                                comboSum = comboSum + allSimils[firstName][state+state2] # try to get e.g. allSimils['Jay']['KYMO']
                                comboCount = comboCount + 1
                            except:
                                pass
                        comboAverage = comboSum/comboCount
                        comboSum = 0
                        comboCount = 0
                        sortedWriter.writerow([state + ' - ' + state2,comboAverage])
                        #print(comboAverage)
                        comboAverage = 0
        print("Data written to 'similaritysortedtest.csv'")
        print()




    ################# COMPARING STATES TO ONE STATE: MAP GIMP CODE ###############################

    # [operation 5]

    elif userInput.startswith('compare states to'):     # compare all states to one state
        focalState = userInput.replace('compare states to ','')

        fileToWrite = open("gimpCode/gimpCodeExperimental"+userYear+userMF+"_"+focalState+".txt", "w")

        for firstName in sortedLimitedNames:    # for every name in the top 100, sorted by rank...
            similsForOneName.clear()            # clear this dictionary
            for state in resStDevPercDictio[firstName].keys():     # for each state
                for state2 in resStDevPercDictio[firstName].keys(): # for each combo of a state with another
                    if state < state2:
                        similsForOneName[state+state2] = abs(resStDevPercDictio[firstName][state] - resStDevPercDictio[firstName][state2])
            allSimils[firstName] = similsForOneName.copy()

        comboSum = 0
        comboCount = 0
        comboAverage = 0

        fileToWrite.write('img = gimp.image_list()[0]\n')
        fileToWrite.write('orig = pdb.gimp_image_get_layer_by_name(img,\'blank\')\n')
        fileToWrite.write('map = pdb.gimp_layer_copy(orig,FALSE)\n')
        fileToWrite.write('pdb.gimp_image_insert_layer(img,map,None,0)\n')
        fileToWrite.write('pdb.gimp_item_set_name(map,\'similarity to ' + focalState + '\')\n')
        fileToWrite.write('pdb.gimp_context_set_paint_mode(30)\n')        # mode 30 is Multiply
        fileToWrite.write('pdb.gimp_context_set_sample_threshold_int(111)\n') # set threshold to 111
        fileToWrite.write('pdb.gimp_context_set_foreground((255,0,0))\n') #sets color to greenSelf
        fileToWrite.write(printingDictio[focalState])


        for state in all50States:     # for each state...
            #print('Starting with ' + state)
            for state2 in all50States:     # for each state...
                if state < state2 and (focalState == state or focalState == state2):
                    #print('...and ' + state2)
                    for firstName in sortedLimitedNames:    # for each name in the top 100 names...
                        try:
                            comboSum = comboSum + allSimils[firstName][state+state2] # try to get e.g. allSimils['Jay']['KYMO']
                            comboCount = comboCount + 1
                        except:
                            pass

                    comboAverage = comboSum/comboCount
                    comboSum = 0
                    comboCount = 0

                    if state == focalState:
                        nonfocalState = state2
                    else:
                        nonfocalState = state

                    if comboAverage < 0.5:                 # red to yellow range
                        colorGIMPstring = '(255,'+str(int(comboAverage*510))+',0)'
                    elif comboAverage < 1:                 # yellow to green range
                        colorGIMPstring = '('+str(int(255-(comboAverage-0.5)*510))+',255,0)'
                    elif comboAverage < 1.5:               # green to cyan range
                        colorGIMPstring = '(0,255,'+str(int((comboAverage-1)*510))+')'
                    elif comboAverage < 2:                 # cyan to blue range
                        colorGIMPstring = '(0,'+str(int(255-(comboAverage-1.5)*510))+',255)'
                    else:
                        colorGIMPstring = '(0,0,0)'

                    #fileToWrite.write('pdb.gimp_context_set_foreground(('+str(round(255*comboAverage/2.5))+',255,'+str(round(255*comboAverage/2.5))+'))\n')

                    fileToWrite.write('pdb.gimp_context_set_foreground('+colorGIMPstring+')\n')
                    fileToWrite.write(printingDictio[nonfocalState])




    ################# TOP 100 NAMES, MAKING MAPS GIMP CODE ###############################

    # [operation 3]

    elif userInput.startswith('top100'):        # makes GIMP code for 100 maps, one for each of the top 100 names that year:
        #print(nameList)
        fileToWrite = open("gimpCode/gimpCode"+userYear+"top100"+userMF+".txt", "w")

        # Loop through each of the top 100 names.
        for top100Name in sortedLimitedNames:
            red4.clear()
            red3.clear()
            red2.clear()
            red1.clear()
            neutral.clear()
            blue1.clear()
            blue2.clear()
            blue3.clear()
            blue4.clear()
            grayNED.clear()

            # Loop through each state that appears as a key in the current name's entry in the RSPD
            for state in resStDevPercDictio[top100Name].keys():
                if resStDevPercDictio[top100Name][state] > 1.75:
                    red4.append(state)
                elif resStDevPercDictio[top100Name][state] > 1.25:
                    red3.append(state)
                elif resStDevPercDictio[top100Name][state] > 0.75:
                    red2.append(state)
                elif resStDevPercDictio[top100Name][state] > 0.25:
                    red1.append(state)
                elif resStDevPercDictio[top100Name][state] > -0.25:
                    neutral.append(state)
                elif resStDevPercDictio[top100Name][state] > -0.75:
                    blue1.append(state)
                elif resStDevPercDictio[top100Name][state] > -1.25:
                    blue2.append(state)
                elif resStDevPercDictio[top100Name][state] > -1.75:
                    blue3.append(state)
                elif resStDevPercDictio[top100Name][state] < -1.75:
                    blue4.append(state)
            for state in all50States:
                if state not in resStDevPercDictio[top100Name].keys():
                    grayNED.append(state)

            # Start writing the GIMP Python-fu code to the file.
            fileToWrite.write('img = gimp.image_list()[0]\n')
            fileToWrite.write('orig = pdb.gimp_image_get_layer_by_name(img,\'blank\')\n')
            fileToWrite.write('map = pdb.gimp_layer_copy(orig,FALSE)\n')
            fileToWrite.write('pdb.gimp_image_insert_layer(img,map,None,0)\n')
            fileToWrite.write('pdb.gimp_item_set_name(map,\'' + top100Name + '\')\n')
            fileToWrite.write('pdb.gimp_context_set_paint_mode(30)\n')        # mode 30 is Multiply
            fileToWrite.write('pdb.gimp_context_set_sample_threshold_int(111)\n') # set threshold to 111
            fileToWrite.write('pdb.gimp_context_set_foreground((191,0,0))\n')  #sets color to red+4
            for state in red4:
                fileToWrite.write(printingDictio[state])
            fileToWrite.write('pdb.gimp_context_set_foreground((255,0,0))\n')     #sets color to red+3
            for state in red3:
                fileToWrite.write(printingDictio[state])
            fileToWrite.write('pdb.gimp_context_set_foreground((255,140,140))\n')  #sets color to red+2
            for state in red2:
                fileToWrite.write(printingDictio[state])
            fileToWrite.write('pdb.gimp_context_set_foreground((255,219,219))\n') #sets color to red+1
            for state in red1:
                fileToWrite.write(printingDictio[state])
            fileToWrite.write('pdb.gimp_context_set_foreground((230,230,255))\n')  #sets color to blue+1
            for state in blue1:
                fileToWrite.write(printingDictio[state])
            fileToWrite.write('pdb.gimp_context_set_foreground((182,182,255))\n')  #sets color to blue+2
            for state in blue2:
                fileToWrite.write(printingDictio[state])
            fileToWrite.write('pdb.gimp_context_set_foreground((113,113,255))\n')  #sets color to blue+3
            for state in blue3:
                fileToWrite.write(printingDictio[state])
            fileToWrite.write('pdb.gimp_context_set_foreground((0,0,255))\n')  #sets color to blue+4
            for state in blue4:
                fileToWrite.write(printingDictio[state])
            fileToWrite.write('pdb.gimp_context_set_foreground((204,204,204))\n')  #sets color to gray-NED
            for state in grayNED:
                fileToWrite.write(printingDictio[state])

    ################# COMPARE A NAME TO OTHER NAMES, DATA PRINTOUT ###############################

    # [operation 6]

    elif userInput.startswith('compare names to'):
        focalName = userInput.replace('compare names to ','')
        while focalName not in resStDevPercDictio.keys():
            print("Oh dear, that name isn't in our name dictionary. You'll have to try again.")
            userInput = input('>>> ')
            focalName = userInput.replace('compare names to ','')

        focalNameDictio = {}
        for state in resStDevPercDictio[focalName].keys():
            focalNameDictio[state] = resStDevPercDictio[focalName][state]

        print('To compare ' + focalName + ' to names from the same year/sex group as you just chose, press enter. To compare to names from a different year/sex group, enter it in the format: 2000M')
        userInputForComparisonGroup = input('>>> ')
        if userInputForComparisonGroup == "":
            secondaryUserYear = userYear
            secondaryUserMF = userMF
        else:
            secondaryUserYear = userInputForComparisonGroup[0:4]
            secondaryUserMF = userInputForComparisonGroup[4]

        secondaryResStDevPercDictio = {}
        secondaryResStDevPercDictio = processDataUpToRSPD(secondaryUserYear,secondaryUserMF)


        print("Computing comparison coefficients...")
        nameComparisonDictio = {}       # deleting any old contents
        sortedNameComparisons = []      # deleting any old contents
        for firstName, smallDictio in secondaryResStDevPercDictio.items():    # for every name...
            comboSum = 0
            comboCount = 0
            comboAverage = 0
            for state in focalNameDictio.keys():   # for every state that had at least 5 children named the focal name...
                try:
                    comboSum = comboSum + abs(secondaryResStDevPercDictio[firstName][state]-focalNameDictio[state])
                    comboCount = comboCount + 1
                except:
                    #print("The iterating name wasn't found for",state)
                    pass
            try:
                comboAverage = comboSum/comboCount
            except:
                pass
            if comboCount > 24:
                nameComparisonDictio[firstName] = comboAverage


        print('************', 'Names\' index of similarity to ' + focalName)
        sortedNameComparisons = sorted(nameComparisonDictio,key=nameComparisonDictio.get,reverse=False)
        #sortedResidualsPercForOneState = sorted(residualsPercForOneState,key=residualsPercForOneState.get,reverse=True)
        for item in sortedNameComparisons:
            print(item, nameComparisonDictio[item])
        print()



    ############# A SINGLE NAME MAP -- GIMP CODE ############################################

    else:       # [operation 2] original script--for analysis of a single name:

        # If the user has already done this since starting the program, these groupings will be populated. We need to start with blank slates.
        red4.clear()
        red3.clear()
        red2.clear()
        red1.clear()
        neutral.clear()
        blue1.clear()
        blue2.clear()
        blue3.clear()
        blue4.clear()
        grayNED.clear()

        # Create a file with a filename in the format: gimpCode/gimpCodeExperimental1986M.txt
        fileToWrite = open("gimpCode/gimpCode"+userYear+userInput+userMF+".txt", "w")

        # Now loop through all the states that are found as keys in the dictionary of RSPD[name the user input]. For names that are popular enough, that's all states; the less popular a name is, the fewer states are actually found as keys.
        # The value for each state/key found is then sorted into one of nine color groupings. The higher the value, the more popular the name, the darker red the color it will be represented by. The lower the value, the less popular the name, the darker blue.
        for state in resStDevPercDictio[userInput].keys():
            if resStDevPercDictio[userInput][state] > 1.75:
                red4.append(state)
            elif resStDevPercDictio[userInput][state] > 1.25:
                red3.append(state)
            elif resStDevPercDictio[userInput][state] > 0.75:
                red2.append(state)
            elif resStDevPercDictio[userInput][state] > 0.25:
                red1.append(state)
            elif resStDevPercDictio[userInput][state] > -0.25:
                neutral.append(state)
            elif resStDevPercDictio[userInput][state] > -0.75:
                blue1.append(state)
            elif resStDevPercDictio[userInput][state] > -1.25:
                blue2.append(state)
            elif resStDevPercDictio[userInput][state] > -1.75:
                blue3.append(state)
            elif resStDevPercDictio[userInput][state] < -1.75:
                blue4.append(state)
        # print(allBirthsDictio)
        # input()
        # Loop through all states. If a state is not found among the keys for this name for this year, add it to the gray color group.
        for state in all50States:
            if state not in resStDevPercDictio[userInput].keys():
                grayNED.append(state)

        # Display these groups in the console.
        print()
        print("1.75+ SDs from mean: ", red4)
        print("1.25 to 1.75 SDs from mean: ", red3)
        print("0.75 to 1.25 SDs from mean: ", red2)
        print("0.25 to 0.75 SDs from mean: ", red1)
        print("-0.25 to 0.25 SDs from mean: ", neutral)
        print("-0.75 to -0.25 SDs from mean: ", blue1)
        print("-1.25 to -0.75 SDs from mean: ", blue2)
        print("-1.75 to -1.25 SDs from mean: ", blue3)
        print("-1.75- SDs from mean: ", blue4)
        print("States with no data: ", grayNED)
        print()

        # Write Gimp python-fu code to the txt file we specified earlier
        fileToWrite.write('img = gimp.image_list()[0]\n')
        fileToWrite.write('orig = pdb.gimp_image_get_layer_by_name(img,\'blank\')\n')
        fileToWrite.write('map = pdb.gimp_layer_copy(orig,FALSE)\n')
        fileToWrite.write('pdb.gimp_image_insert_layer(img,map,None,0)\n')
        fileToWrite.write('pdb.gimp_item_set_name(map,\'' + userInput + '\')\n')
        #print('map = pdb.gimp_image_get_layer_by_name(img, \'' + userInput + '\')')
        fileToWrite.write('pdb.gimp_context_set_paint_mode(30)\n')        # mode 30 is Multiply
        fileToWrite.write('pdb.gimp_context_set_sample_threshold_int(111)\n') # set threshold to 111--experimentally seems to work well
        fileToWrite.write('pdb.gimp_context_set_foreground((191,0,0))\n')         #sets the color to red+4
        for state in red4:
            fileToWrite.write(printingDictio[state])
        fileToWrite.write('pdb.gimp_context_set_foreground((255,0,0))\n')         #sets the color to red+3
        for state in red3:
            fileToWrite.write(printingDictio[state])
        fileToWrite.write('pdb.gimp_context_set_foreground((255,140,140))\n')         #sets the color to red+2
        for state in red2:
            fileToWrite.write(printingDictio[state])
        fileToWrite.write('pdb.gimp_context_set_foreground((255,219,219))\n')         #sets the color to red+1
        for state in red1:
            fileToWrite.write(printingDictio[state])
        fileToWrite.write('pdb.gimp_context_set_foreground((230,230,255))\n')         #sets the color to blue+1
        for state in blue1:
            fileToWrite.write(printingDictio[state])
        fileToWrite.write('pdb.gimp_context_set_foreground((182,182,255))\n')         #sets the color to blue+2
        for state in blue2:
            fileToWrite.write(printingDictio[state])
        fileToWrite.write('pdb.gimp_context_set_foreground((113,113,255))\n')         #sets the color to blue+3
        for state in blue3:
            fileToWrite.write(printingDictio[state])
        fileToWrite.write('pdb.gimp_context_set_foreground((0,0,255))\n')         #sets the color to blue+4
        for state in blue4:
            fileToWrite.write(printingDictio[state])
        fileToWrite.write('pdb.gimp_context_set_foreground((204,204,204))\n')         #sets the color to gray-NED
        for state in grayNED:
            fileToWrite.write(printingDictio[state])

try:
    fileToWrite.close()
    currentFolder.close()
except:
    pass
