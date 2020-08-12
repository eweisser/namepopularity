import csv
#import xlrd
import os
import time
import statistics

# We want column "stateres" (str2) [column U, or 21st column, index 20, for many years--not guaranteed]:

#column "csex" [column CI, or 87th column, index 86, for many years--not guaranteed]:
#1	male
#2	female

#currentFolder = os.scandir()
userChosenYear = 0
columnForStateCode = 0
columnForSexCode = 0
counterDictionary = {}
#babyCount = 0
MCount = 0
FCount = 0
rowCount = 0
stateList = []
    
userChosenYear = input('What year do you want to count? ')
columnForStateCode = int(input('What index number has the state codes? A good guess is 20. '))
columnForSexCode = int(input('What index number has the sex data? A good guess is 86. '))
print("Results will be output to \"count" + userChosenYear + ".txt\"")

with open("after1994\\natl" + userChosenYear + ".csv") as csv_file:
    reader = csv.reader(csv_file, delimiter=",")
    for row in reader:      # for every row in the CSV file...
        rowCount = rowCount + 1
        currentValues = counterDictionary.get(row[columnForStateCode],[0,0,0])      # row[20] for year 1999
        currentValues[0] = currentValues[0]+1
        if row[columnForSexCode] == '1':                # row[86] for year 1999
            currentValues[1] = currentValues[1]+1
        if row[columnForSexCode] == '2':
            currentValues[2] = currentValues[2]+1
        counterDictionary[row[columnForStateCode]] = currentValues

stateList = ['AL','AK','AZ','AR','CA','CO','CT','DC','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']
codeToPrintFemaleCount = "{'"
codeToPrintMaleCount = "{'"
codeToPrintCombinedCount = "{'"
    
# first the girls:
for x in range(51):
    try:
        if x <= 8:
            codeToPrintFemaleCount = codeToPrintFemaleCount + stateList[x] + "':" + str(counterDictionary["0"+str(x+1)][2]) + ",'"
        else:
            codeToPrintFemaleCount = codeToPrintFemaleCount + stateList[x] + "':" + str(counterDictionary[str(x+1)][2]) + ",'"
    except:
        print("Tried to print when x = " + str(x))
        #pass

codeToPrintFemaleCount = codeToPrintFemaleCount.rstrip(",'")
codeToPrintFemaleCount = codeToPrintFemaleCount + "}"

# now for the boys:
for x in range(51):
    try:
        if x <= 8:
            codeToPrintMaleCount = codeToPrintMaleCount + stateList[x] + "':" + str(counterDictionary["0"+str(x+1)][1]) + ",'"
        else:
            codeToPrintMaleCount = codeToPrintMaleCount + stateList[x] + "':" + str(counterDictionary[str(x+1)][1]) + ",'"
    except:
        print("Tried to print when x = " + str(x))
        #pass

codeToPrintMaleCount = codeToPrintMaleCount.rstrip(",'")
codeToPrintMaleCount = codeToPrintMaleCount + "}"

# now combined:
for x in range(51):
    try:
        if x <= 8:
            codeToPrintCombinedCount = codeToPrintCombinedCount + stateList[x] + "':" + str(counterDictionary["0"+str(x+1)][0]) + ",'"
        else:
            codeToPrintCombinedCount = codeToPrintCombinedCount + stateList[x] + "':" + str(counterDictionary[str(x+1)][0]) + ",'"
    except:
        print("Tried to print when x = " + str(x))
        #pass

codeToPrintCombinedCount = codeToPrintCombinedCount.rstrip(",'")
codeToPrintCombinedCount = codeToPrintCombinedCount + "}"

fileToPrintTo = open("count"+userChosenYear+".txt", "w")
fileToPrintTo.write("FEMALE\n"+codeToPrintFemaleCount+"\nMALE\n"+codeToPrintMaleCount+"\nTOTAL\n"+codeToPrintCombinedCount)

#currentFolder.close()