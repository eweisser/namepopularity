import csv
#import xlrd
import os
import time
import statistics

# What does this file do?
    # It reads CSV files, specifically...
    # It tries to open files in the folder 'bigCSVs', with the filename format like 'natl1986.csv'.
            # These files contain data on every baby born in the US in one year. There is always one column of the data containing either 1 (signifying a male) or 2 (signifying a female). This column has the heading 'csex'.
            # There is also always one column that codes (presumably) the state the baby's mother resided in. '01' codes Alabama, while '51' codes Wyoming. '09' codes the District of Columbia. Numbers over 51 code for non-state territories of the United States and foreign countries, with some countries receiving specific codes. At the time of this writing (5.23.2021) it is my impression that the portion of this coding scheme limited to US states remains consistent as far back in time as the admission of Hawaii as the 50th state, but I have not conclusively verified this. It is also worth pointing out that the numeric codes for each state (plus the District of Columbia) are assigned in alphabetical order corresponding to the states' full names, rather than the states' widely-recognized two-letter USPS abbreviations. These abbreviations are, in fact, used elsewhere in this script. In the data, this column has the heading 'stateres'.
                    # The data files contain multiple columns that code for locations relating to the child's mother. Some of these are very different measures, either more precise (like county-level) or less precise (like region), but others are, likewise, encodings of states. The latter includes (but is not necessarily limited to):
                        # "Expanded State of Residence", with a very similar coding scheme for the residence of the baby's mother, changed slightly to code New York City separately from New York state outside New York City (heading: stresexp)
                        # "State Subcode of Residence", with a coding scheme based on geographical groupings rather than alphabetical order (stsubres)
                        # "State of Occurrence", with a coding scheme identical to the stateres column, but recording instead the actual location of the child's birth (statenat)
                        # "Expanded State of Occurrence", just like "Expanded State of Residence" but reflecting the actual location of the child's birth (stnatexp)
                        # "State Subcode of Occurrence", with a coding scheme identical to the stsubres column, but again, recording the actual location of the child's birth (stsubocc)
                        # "Mother's Place of Birth", using the alphabetical coding scheme (mplbir)
                        # "State of Occurrence (FIPS)", with a coding scheme making use of FIPS (Federal Information Processing Standards) codes. This is similar to the alphabetical coding scheme described earlier, but it is not identical, and is less intutive, skipping over some numbers so that Wyoming is coded as '56'. The point of this is not clear to me at the time of writing (stoccfip)
                        # "State of Residence (FIPS)", see the previous entry (stresfip)
            # The index numbers of the two relevant columns are NOT consistent between years, however.
    # Using the two relevant columns 'csex' and 'stateres', it counts the number of male births for each state respectively, and female births for each state respectively.
    # It also counts the total number of births recorded for each state, using only the 'stateres' column.
            # If each birth (row of data) has either a '1' or a '2', then, the count of male births plus the count of female births should equal count of the total number of births, for each state individually. To reiterate: the figure for the total number of births is not calculated simply by adding the count of male births to the count of female births. If the male plus female sum is not equal to the total number of births, any of the following may have occurred:
                    # The program contains an error.
                    # The data contain some birth records with neither a '1' nor a '2' in the column with the 'csex' header. This may be an error in the data recording or collection, or it may reflect intersex births. As of this writing, I have not found any errors in the data, nor any references in the documentation to intersex births.
    # It uses these counts to build strings formatted to be Python-readable code, specifically as Python dictionaries.
    # It tries to output .txt files containing these strings, with a filename formatted like 'count1986.txt'.
    # It replaces an original file readUniversal.py. It has a feature that lets you 'sample' the data, reading one line at a time, before counting the whole file. The point of this is to let the user try to determine for themselves which columns correspond to the desired information.

    # I plan to soon make this program find the proper 'csex' and 'stateres' columns itself, but this has not yet been written.

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
columnForStateCode = -1
columnForSexCode = -1

userChosenYear = input('Choose a year to count. If you just want to read the first few lines, type \' sample\' after the year itself. ')
if userChosenYear.endswith('sample'):
    pass
else:
    # columnForStateCode = int(input('What index number has the state codes? A good guess is 20. '))
    # columnForSexCode = int(input('What index number has the sex data? A good guess is 86. '))
    print("Results will be output to \"count" + userChosenYear + ".txt\"")



with open("bigCSVs\\natl" + userChosenYear[0:4] + ".csv") as csv_file:
    reader = csv.reader(csv_file, delimiter=",")

    for row in reader:
        rowCount = rowCount + 1
        if rowCount > 3:
            break
        for i in range(len(row)):
            if row[i] == "stateres":
                columnForStateCode = i
            if row[i] == "csex":
                columnForSexCode = i
            if columnForStateCode > -1 and columnForSexCode > -1:
                break

    rowCount = 0

    for row in reader:      # for every row in the CSV file...
        rowCount = rowCount + 1                 # add 1 to the rowCount

        if userChosenYear.endswith('sample'):   # if the user asked for a 'sample'...
            for i in range(len(row)):           # for every index number in the array made from the row...
                print(i,row[i])                     # print the index number and the contents of row at that index
            userReadyToContinue = input('Press ENTER when you are ready to read the next line. ')

        else:               # if the user did not ask for a sample...
            currentValues = counterDictionary.get(row[columnForStateCode],[0,0,0])      # reminder how .get() works for Python dictionaries: the first parameter is a key in counterDictionary. If the key is found, return the value. If the key isn't found, return the second parameter. Here, the keys are the codes for states as found in STATERES. If the state/key for this row has appeared before, get its current counts. If this is the first time this state/key has been found, return [0,0,0].
            currentValues[0] = currentValues[0]+1
            if row[columnForSexCode] == '1':
                currentValues[1] = currentValues[1]+1
            if row[columnForSexCode] == '2':
                currentValues[2] = currentValues[2]+1
            counterDictionary[row[columnForStateCode]] = currentValues          # set the value for the key (state) found for this row to be the currentValues array (create the key/value pair if it doesn't exist)
            # print(row[columnForStateCode])
            # print(currentValues)
            # input()
    #print(counterDictionary)

stateList = ['AL','AK','AZ','AR','CA','CO','CT','DE','DC','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']
codeToPrintFemaleCount = "{'"
codeToPrintMaleCount = "{'"
codeToPrintCombinedCount = "{'"


# In this section, we'll double-check that the male plus female numbers equal the total for each state.
for stateNumber in counterDictionary:
        counts = counterDictionary[stateNumber]
        if counts[0] == (counts[1]+counts[2]):
            pass
            # print(counts[0],"is the same as",counts[1] + counts[2])
        else:
            print("CALCULATION WARNING:")
            print("For state with ID",stateNumber,"totals do not match")
            print("Total births counted:",counts[0])
            print("Male births counted:",counts[1])
            print("Female births counted:",counts[2])
            input()







# PREPARING THE STRINGS TO WRITE TO THE FILE

# first the girls:
for x in range(51):
    try:
        if x <= 8:      # this is necessary because the states with STATERES code numbers less than 10 are coded with a leading zero.
            codeToPrintFemaleCount = codeToPrintFemaleCount + stateList[x] + "':" + str(counterDictionary["0"+str(x+1)][2]) + ",'"
        else:
            codeToPrintFemaleCount = codeToPrintFemaleCount + stateList[x] + "':" + str(counterDictionary[str(x+1)][2]) + ",'"
        # We're going through each number from 0 to 50. We add 1, getting 1 to 51. For 1 to 9 (originally 0 to 8), we add a leading zero. So now we have 01 to 51. We treat this as a key in counterDictionary and get the value for this key. It's an array. We get the value at index 2 of the array (index 2 is the female total). Convert this number to a string. The key 'stateres' is never retrieved.
    except:
        print("Tried to print when x = " + str(x))
        #pass

codeToPrintFemaleCount = codeToPrintFemaleCount.rstrip(",'")
codeToPrintFemaleCount = codeToPrintFemaleCount + "}"

# now for the boys:
for x in range(51):
    try:
        if x <= 8:      # this is necessary because the states with STATERES code numbers less than 10 are coded with a leading zero.
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
        if x <= 8:      # this is necessary because the states with STATERES code numbers less than 10 are coded with a leading zero.
            codeToPrintCombinedCount = codeToPrintCombinedCount + stateList[x] + "':" + str(counterDictionary["0"+str(x+1)][0]) + ",'"
        else:
            codeToPrintCombinedCount = codeToPrintCombinedCount + stateList[x] + "':" + str(counterDictionary[str(x+1)][0]) + ",'"
    except:
        print("Tried to print when x = " + str(x))
        #pass

codeToPrintCombinedCount = codeToPrintCombinedCount.rstrip(",'")
codeToPrintCombinedCount = codeToPrintCombinedCount + "}"

wantToOutput = input('If you want to output the counts to a text file, enter \'y\' or \'yes\': ')

if wantToOutput == 'y' or wantToOutput == 'yes':
    fileToPrintTo = open("count"+userChosenYear+".txt", "w")
    fileToPrintTo.write("FEMALE\n"+codeToPrintFemaleCount+"\nMALE\n"+codeToPrintMaleCount+"\nTOTAL\n"+codeToPrintCombinedCount)

#currentFolder.close()
