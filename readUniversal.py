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

userChosenYear = input('Choose a year to count. If you just want to read the first few lines, type \' sample\' after the year itself. ')
columnForStateCode = int(input('What index number has the state codes? A good guess is 20. '))
columnForSexCode = int(input('What index number has the sex data? A good guess is 86. '))
print("Results will be output to \"count" + userChosenYear + ".txt\"")




with open("bigCSVs\\natl" + userChosenYear[0:4] + ".csv") as csv_file:
    reader = csv.reader(csv_file, delimiter=",")
    for row in reader:      # for every row in the CSV file...
        rowCount = rowCount + 1
        if userChosenYear.endswith('sample'):
            for i in range(len(row)):
                print(i,row[i])
            userReadyToContinue = input('Are you ready to read the next line? ')
        else:
            currentValues = counterDictionary.get(row[columnForStateCode],[0,0,0])      # row[20] for year 1999
            currentValues[0] = currentValues[0]+1
            if row[columnForSexCode] == '1':                # row[86] for year 1999
                currentValues[1] = currentValues[1]+1
            if row[columnForSexCode] == '2':
                currentValues[2] = currentValues[2]+1
            counterDictionary[row[columnForStateCode]] = currentValues

stateList = ['AL','AK','AZ','AR','CA','CO','CT','DE','DC','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']
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
