import csv
#import xlrd
import os
import time
import statistics

# If the dictionary 'allBirthsDictio' starts with a value of 30524 for Alabama, you still have the values from 1986/males. If this is supposed to be a different file, some or all values will need to be changed.

currentFolder = os.scandir()
allData = []    # this will hold all the data--except we'll restrict it the relevant year and gender--so we don't have to reread files
nameList = []   # this has all the relevant first names, each only ONCE
smallDictio = {}
byNameDictio = {}
allBirthsDictio = {'AL':28998,'AK':4890,'AR':18259,'AZ':42737,'CA':258922,'CO':33223,'CT':20423,'DE':5397,'FL':100227,'GA':65272,'HI':8289,'ID':10277,'IL':88154,'IN':41712,'IA':18197,'KS':19313,'KY':26335,'LA':31629,'ME':6640,'MD':35724,'MA':39411,'MI':63491,'MN':33181,'MS':20243,'MO':36531,'MT':5428,'NE':12416,'NV':15880,'NH':6952,'NJ':55781,'NM':13790,'NY':122659,'NC':57294,'ND':3711,'OH':72481,'OK':24480,'OR':22097,'PA':69716,'RI':6276,'SC':26725,'SD':5187,'TN':38078,'TX':182249,'UT':24017,'VT':3108,'VA':48950,'WA':38557,'WV':10021,'WI':33541,'WY':3175}
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
printingDictio = {'AL':'pdb.gimp_drawable_edit_bucket_fill(map,0,533,333)','AK':'pdb.gimp_drawable_edit_bucket_fill(map,0,90,400)\npdb.gimp_drawable_edit_bucket_fill(map,0,165,430)\npdb.gimp_drawable_edit_bucket_fill(map,0,90,462)\npdb.gimp_drawable_edit_bucket_fill(map,0,38,439)\npdb.gimp_drawable_edit_bucket_fill(map,0,186,453)\npdb.gimp_drawable_edit_bucket_fill(map,0,44,484)\npdb.gimp_drawable_edit_bucket_fill(map,0,31,491)\npdb.gimp_drawable_edit_bucket_fill(map,0,167,440)\npdb.gimp_drawable_edit_bucket_fill(map,0,173,438)\npdb.gimp_drawable_edit_bucket_fill(map,0,27,411)\npdb.gimp_drawable_edit_bucket_fill(map,0,173,446)\npdb.gimp_drawable_edit_bucket_fill(map,0,180,444)\npdb.gimp_drawable_edit_bucket_fill(map,0,184,445)','AR':'pdb.gimp_drawable_edit_bucket_fill(map,0,450,300)','AZ':'pdb.gimp_drawable_edit_bucket_fill(map,0,160,300)','CA':'pdb.gimp_drawable_edit_bucket_fill(map,0,60,240)','CO':'pdb.gimp_drawable_edit_bucket_fill(map,0,260,230)','CT':'pdb.gimp_drawable_edit_bucket_fill(map,0,700,140)','DE':'pdb.gimp_drawable_edit_bucket_fill(map,0,677,200)','FL':'pdb.gimp_drawable_edit_bucket_fill(map,0,610,380)','GA':'pdb.gimp_drawable_edit_bucket_fill(map,0,585,330)','HI':'pdb.gimp_drawable_edit_bucket_fill(map,0,268,456)\npdb.gimp_drawable_edit_bucket_fill(map,0,249,429)\npdb.gimp_drawable_edit_bucket_fill(map,0,212,412)\npdb.gimp_drawable_edit_bucket_fill(map,0,177,398)\npdb.gimp_drawable_edit_bucket_fill(map,0,236,421)\npdb.gimp_drawable_edit_bucket_fill(map,0,236,428)','ID':'pdb.gimp_drawable_edit_bucket_fill(map,0,150,120)','IL':'pdb.gimp_drawable_edit_bucket_fill(map,0,480,200)','IN':'pdb.gimp_drawable_edit_bucket_fill(map,0,530,200)','IA':'pdb.gimp_drawable_edit_bucket_fill(map,0,420,170)','KS':'pdb.gimp_drawable_edit_bucket_fill(map,0,360,240)','KY':'pdb.gimp_drawable_edit_bucket_fill(map,0,550,240)','LA':'pdb.gimp_drawable_edit_bucket_fill(map,0,450,380)','ME':'pdb.gimp_drawable_edit_bucket_fill(map,0,730,60)','MD':'pdb.gimp_drawable_edit_bucket_fill(map,0,653,193)\npdb.gimp_drawable_edit_bucket_fill(map,0,622,195)\npdb.gimp_drawable_edit_bucket_fill(map,0,631,192)','MA':'pdb.gimp_drawable_edit_bucket_fill(map,0,708,124)','MI':'pdb.gimp_drawable_edit_bucket_fill(map,0,540,150)\npdb.gimp_drawable_edit_bucket_fill(map,0,490,90)','MN':'pdb.gimp_drawable_edit_bucket_fill(map,0,410,100)','MS':'pdb.gimp_drawable_edit_bucket_fill(map,0,490,340)','MO':'pdb.gimp_drawable_edit_bucket_fill(map,0,450,240)','MT':'pdb.gimp_drawable_edit_bucket_fill(map,0,230,80)','NE':'pdb.gimp_drawable_edit_bucket_fill(map,0,350,190)','NV':'pdb.gimp_drawable_edit_bucket_fill(map,0,100,200)','NH':'pdb.gimp_drawable_edit_bucket_fill(map,0,705,100)','NJ':'pdb.gimp_drawable_edit_bucket_fill(map,0,680,160)','NM':'pdb.gimp_drawable_edit_bucket_fill(map,0,250,310)','NY':'pdb.gimp_drawable_edit_bucket_fill(map,0,666,127)\npdb.gimp_drawable_edit_bucket_fill(map,0,694,157)','NC':'pdb.gimp_drawable_edit_bucket_fill(map,0,640,270)','ND':'pdb.gimp_drawable_edit_bucket_fill(map,0,340,80)','OH':'pdb.gimp_drawable_edit_bucket_fill(map,0,570,190)','OK':'pdb.gimp_drawable_edit_bucket_fill(map,0,380,290)','OR':'pdb.gimp_drawable_edit_bucket_fill(map,0,80,100)','PA':'pdb.gimp_drawable_edit_bucket_fill(map,0,640,170)','RI':'pdb.gimp_drawable_edit_bucket_fill(map,0,714,133)','SC':'pdb.gimp_drawable_edit_bucket_fill(map,0,620,300)','SD':'pdb.gimp_drawable_edit_bucket_fill(map,0,340,130)','TN':'pdb.gimp_drawable_edit_bucket_fill(map,0,530,280)','TX':'pdb.gimp_drawable_edit_bucket_fill(map,0,360,360)','UT':'pdb.gimp_drawable_edit_bucket_fill(map,0,180,210)','VT':'pdb.gimp_drawable_edit_bucket_fill(map,0,690,90)','VA':'pdb.gimp_drawable_edit_bucket_fill(map,0,640,230)\npdb.gimp_drawable_edit_bucket_fill(map,0,677,220)','WA':'pdb.gimp_drawable_edit_bucket_fill(map,0,100,40)','WV':'pdb.gimp_drawable_edit_bucket_fill(map,0,600,220)','WI':'pdb.gimp_drawable_edit_bucket_fill(map,0,470,120)','WY':'pdb.gimp_drawable_edit_bucket_fill(map,0,240,150)'}

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
                if row[1] == "F" and row[2] == "2002" and not row[0] == "DC":
                    row[4] = int(row[4])/allBirthsDictio[row[0]]   # turn the raw number into the percentage of babies with that name
                    allData.append(row)
                    if row[3] not in nameList:          # if the name isn't in the list already...
                        nameList.append(row[3])             # add it to the end of the list



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



        print('img = gimp.image_list()[0]')
        print('orig = pdb.gimp_image_get_layer_by_name(img,\'blank\')')
        print('map = pdb.gimp_layer_copy(orig,FALSE)')
        print('pdb.gimp_image_insert_layer(img,map,None,0)')
        print('pdb.gimp_item_set_name(map,\'' + userChosenName + '\')')
        #print('map = pdb.gimp_image_get_layer_by_name(img, \'' + userChosenName + '\')')
        print('pdb.gimp_context_set_paint_mode(30)')        # mode 30 is Multiply
        print('pdb.gimp_context_set_sample_threshold_int(111)') # set threshold to 111--experimentally seems to work well
        print('pdb.gimp_context_set_foreground((191,0,0))')         #sets the color to red+4
        for state in red4:
            print(printingDictio[state])
        print('pdb.gimp_context_set_foreground((255,0,0))')         #sets the color to red+3
        for state in red3:
            print(printingDictio[state])
        print('pdb.gimp_context_set_foreground((255,140,140))')         #sets the color to red+2
        for state in red2:
            print(printingDictio[state])
        print('pdb.gimp_context_set_foreground((255,219,219))')         #sets the color to red+1
        for state in red1:
            print(printingDictio[state])
        print('pdb.gimp_context_set_foreground((230,230,255))')         #sets the color to blue+1
        for state in blue1:
            print(printingDictio[state])
        print('pdb.gimp_context_set_foreground((182,182,255))')         #sets the color to blue+2
        for state in blue2:
            print(printingDictio[state])
        print('pdb.gimp_context_set_foreground((113,113,255))')         #sets the color to blue+3
        for state in blue3:
            print(printingDictio[state])
        print('pdb.gimp_context_set_foreground((0,0,255))')         #sets the color to blue+4
        for state in blue4:
            print(printingDictio[state])
        print('pdb.gimp_context_set_foreground((204,204,204))')         #sets the color to gray-NED
        for state in grayNED:
            print(printingDictio[state])    





#loc = "state first names 2 boys.xls"
#wb = xlrd.open_workbook("state first names 2 boys.xls")
#sheet = wb.sheet_by_index(1)
#print(sheet.cell_value(2, 2))

currentFolder.close()