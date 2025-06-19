import re
import os
import math
import pandas as pd
from distutils.dir_util import copy_tree as cptr
import fileinput

hot_folder = "D:\\02_NAUKA\\STRONA-CWICZENIA-FRANCUSKIE\\VERIFIED_2022-10-10_2\\missing-element\\hot_folder"
css_path = "D:\\02_NAUKA\\STRONA-CWICZENIA-FRANCUSKIE\\VERIFIED_2022-10-10_2\\missing-element\\dist"
parent_directory = "D:\\02_NAUKA\\STRONA-CWICZENIA-FRANCUSKIE\\VERIFIED_2022-10-10_2"

#working methods
def finishJSArrayString(string):
    pattern = r"\,\s$"
    return re.sub(pattern, " ]", string)

def pickRandomDesign(path):
    css_files = os.listdir(path)
    cssToUse = 0
    with open("D:\\02_NAUKA\\STRONA-CWICZENIA-FRANCUSKIE\\VERIFIED_2022-10-10_2\\automatyzacja-python\\cssUsed.txt") as cssMemory:
        lastCssUsed = int(cssMemory.read())
    if lastCssUsed < css_files.count:
        cssToUse = lastCssUsed + 1    
    with open("D:\\02_NAUKA\\STRONA-CWICZENIA-FRANCUSKIE\\VERIFIED_2022-10-10_2\\automatyzacja-python\\cssUsed.txt", "w") as cssMemory:
        cssMemory.write(str(cssToUse))
    print("dist\\" + css_files[cssToUse])
    return "dist\\" + css_files[cssToUse]

#The csv file to be processed should have a specific file name structure and should be utf-8 encoded.
#<exercice-type>_otherContent.csv

hf_files = os.listdir(hot_folder)
print(hf_files)

for file in hf_files:
    if file.endswith('csv'):
        #if file.find("missing-element") > -1 or file.find("pytanie-odpowiedz") > -1:
        if file.find("missing-element") > -1:
            df = pd.read_csv(os.path.join(hot_folder, file),
                 delimiter=';',
                 encoding='utf-8',
                 header=0) 
            
            #creating first version of strings which will be passed on to the js file with parameters for creating the html index file.
            #firstPart = []
            #secondPart = []
            #missingElement = []
            #hints = [] 

            firstPartString = "firstPart = [ "
            secondPartString = "secondPart = [ "
            missingElementString = "missingElement = [ "
            hintsString = "hints = [ "

            for array in df.values:
                firstPartString = firstPartString + f'"{array[0]}", '
                secondPartString = secondPartString + f'"{array[1]}", '
                missingElementString = missingElementString + f'"{array[2]}", '
                hintsString = hintsString + f'"{array[3]}", '
            
            firstPartString = finishJSArrayString(firstPartString)
            secondPartString = finishJSArrayString(secondPartString)
            missingElementString = finishJSArrayString(missingElementString)
            hintsString = finishJSArrayString(hintsString)

            print(firstPartString)
            print(secondPartString)
            print(missingElementString)
            print(hintsString)

            #check the exercice number
            with open('exerciceNumber.txt') as numRepoRead:
                exNumber = int(numRepoRead.read()) + 1

            #create the target folder
            tgtDirectoryNameString = "missing-element-cw" + str(exNumber)            
            tgtDirectoryName = os.path.join(parent_directory, tgtDirectoryNameString)
            #parentDirectory = os.path.abspath(os.getcwd())
            os.mkdir(os.path.join(parent_directory, tgtDirectoryName))
            #copy files from src folder to tgt folder
            cptr(os.path.join(parent_directory, 'missing-element'), tgtDirectoryName)
            #modify the missing-element.js
            with open(os.path.join(tgtDirectoryName, "missing-element.js"), 'r', encoding='utf-8') as jsf:
                content = jsf.read()
                content = content.replace("firstPart = []", firstPartString)
                content = content.replace("secondPart = []", secondPartString)
                content = content.replace("missingElement = []", missingElementString)
                content = content.replace("hints = []", hintsString)

            with open(os.path.join(tgtDirectoryName, "missing-element.js"), 'w', encoding='utf-8') as jsfw:
                 jsfw.write(content)
                           
            #write exercice number
            with open('exerciceNumber.txt', 'w') as numRepoWrite:
                numRepoWrite.write(str(exNumber))

            #

print("Done!")