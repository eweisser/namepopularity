import csv
#import xlrd
import os
import time
import statistics

# ! Notes for 2000-F:
# None. Continue on course using 2000-M as the template.

# If the dictionary 'allBirthsDictio' starts with a value of 32330 for Alabama, you still have the values from 2000/males. If this is supposed to be a different file, some or all values will need to be changed.

# Also don't forget to change:
    # "F" / "M" flag in row[1] == "M" (appears twice)
    # year in row[2] == "####" (appears twice)
    # output .txt file name, year and sex

currentFolder = os.scandir()
allData = []    # this will hold all the data--except we'll restrict it the relevant year and gender--so we don't have to reread files
nameList = []   # this has all the relevant first names, each only ONCE
smallDictio = {}    
byNameDictio = {}
allBirthsDictio = {'AL':30969,'AK':4820,'AZ':41680,'AR':18459,'CA':259550,'CO':31957,'CT':20906,'DE':5321,'FL':99963,'GA':65107,'HI':8412,'ID':9966,'IL':90733,'IN':42591,'IA':18777,'KS':19284,'KY':27145,'LA':33426,'ME':6626,'MD':36400,'MA':39852,'MI':66608,'MN':32993,'MS':21500,'MO':37378,'MT':5375,'NE':12032,'NV':14853,'NH':6974,'NJ':56404,'NM':13334,'NY':126022,'NC':58991,'ND':3682,'OH':75822,'OK':24144,'OR':22288,'PA':71603,'RI':5971,'SC':27389,'SD':5018,'TN':38879,'TX':177795,'UT':22983,'VT':3141,'VA':48444,'WA':39456,'WV':10111,'WI':33872,'WY':3106}
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

#def allRed4():
    

# row[0] is state, e.g. "AK"
# row[1] is gender, e.g. "F"
# row[2] is year, e.g. "1973"
# row[3] is name, e.g. "Jeanette"
# row[4] is number of babies, e.g. "63"


for entry in currentFolder:             # first, we need to make the list of names
    if entry.name.endswith('.TXT'):     # consider only the .txt files
        with open(entry.name) as csv_file:      # let's open that .txt file as a CSV file
            csv_reader = csv.reader(csv_file, delimiter=",")
            for row in csv_reader:          # take a row, and--
                if row[1] == "F" and row[2] == "2000":
                    rawNum = row[4]                     # save the actual number of records as 'rawNum'
                    simpleCount.setdefault(row[3],0)    # put that into the simpleCount dictionary
                    simpleCount[row[3]] = simpleCount[row[3]] + int(rawNum) # upd the simpleCount dictionary
                if row[1] == "F" and row[2] == "2000" and not row[0] == "DC":
                    row[4] = int(row[4])/allBirthsDictio[row[0]]   # turn the raw number into the percentage of babies with that name
                    allData.append(row)
                    if row[3] not in nameList:          # if the name isn't in the list already...
                        nameList.append(row[3])             # add it to the end of the list

#print(simpleCount)
sortedNames = sorted(simpleCount,key=simpleCount.get,reverse=True)
sortedLimitedNames = sortedNames[0:100]
#print(sortedLimitedNames)


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
for firstName in resStDevPercDictio.keys():
    for state in resStDevPercDictio[firstName].keys():
        if byNameDictio[firstName]['pStDev'] != 0:
            resStDevPercDictio[firstName][state] = residualsDictio[firstName][state] / byNameDictio[firstName]['pStDev']
    resStDevPercDictio[firstName].pop('mean')
    resStDevPercDictio[firstName].pop('pStDev')

#Excellent. That's the main task. Now we can sort them a little.

fileToWrite = open("gimpCode/gimpCode2000F.txt", "w")

while True:
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
    userChosenName = input('Choose a name, or a state. If you choose a state, write it like \'state PA\': ')
    if userChosenName.startswith('state'):
        residualsPercForOneState = {}
        for firstName in resStDevPercDictio.keys():
            for state in resStDevPercDictio[firstName].keys():
                if userChosenName.strip().endswith(state):
                    residualsPercForOneState[firstName] = resStDevPercDictio[firstName][state]
        print('*************', userChosenName, 'percentages of standard deviation')
        sortedResidualsPercForOneState = sorted(residualsPercForOneState,key=residualsPercForOneState.get,reverse=True)
        for item in sortedResidualsPercForOneState:
            print(item, residualsPercForOneState[item])
       
    elif len(userChosenName) < 1 or userChosenName == "x" or userChosenName == "q":
        break
    elif userChosenName.startswith('top100'):
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
            for state in allBirthsDictio.keys():
                if state not in resStDevPercDictio[top100Name].keys():
                    grayNED.append(state)

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



# older style:


    else:
        for state in resStDevPercDictio[userChosenName].keys():
            if resStDevPercDictio[userChosenName][state] > 1.75:
                red4.append(state)
            elif resStDevPercDictio[userChosenName][state] > 1.25:
                red3.append(state)
            elif resStDevPercDictio[userChosenName][state] > 0.75:
                red2.append(state)
            elif resStDevPercDictio[userChosenName][state] > 0.25:
                red1.append(state)
            elif resStDevPercDictio[userChosenName][state] > -0.25:
                neutral.append(state)
            elif resStDevPercDictio[userChosenName][state] > -0.75:
                blue1.append(state)
            elif resStDevPercDictio[userChosenName][state] > -1.25:
                blue2.append(state)
            elif resStDevPercDictio[userChosenName][state] > -1.75:
                blue3.append(state)
            elif resStDevPercDictio[userChosenName][state] < -1.75:
                blue4.append(state)
        for state in allBirthsDictio.keys():
            if state not in resStDevPercDictio[userChosenName].keys():
                grayNED.append(state)

        fileToWrite.write('img = gimp.image_list()[0]\n')
        fileToWrite.write('orig = pdb.gimp_image_get_layer_by_name(img,\'blank\')\n')
        fileToWrite.write('map = pdb.gimp_layer_copy(orig,FALSE)\n')
        fileToWrite.write('pdb.gimp_image_insert_layer(img,map,None,0)\n')
        fileToWrite.write('pdb.gimp_item_set_name(map,\'' + userChosenName + '\')\n')
        #print('map = pdb.gimp_image_get_layer_by_name(img, \'' + userChosenName + '\')')
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

        
fileToWrite.close()
currentFolder.close()