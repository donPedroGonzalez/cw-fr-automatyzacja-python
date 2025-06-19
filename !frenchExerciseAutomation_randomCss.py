import re
import os
import math
import pandas as pd
from distutils.dir_util import copy_tree as cptr
import fileinput

#hot_folder = "D:\\02_NAUKA\\STRONA-CWICZENIA-FRANCUSKIE\\VERIFIED_2022-10-10_2\\missing-element\\hot_folder"
#css_path = "D:\\02_NAUKA\\STRONA-CWICZENIA-FRANCUSKIE\\VERIFIED_2022-10-10_2\\missing-element\\dist"

hot_folder = "D:\\02_NAUKA\\STRONA-CWICZENIA-FRANCUSKIE\\VERIFIED_2022-10-10_2\\pytanie-odpowiedz\\hot_folder"
css_path = "D:\\02_NAUKA\\STRONA-CWICZENIA-FRANCUSKIE\\VERIFIED_2022-10-10_2\\pytanie-odpowiedz\\dist"


tgtDirectoryName = parentDirectory = ""


#working methods
def finishJSArrayString(string):
    pattern = r"\,\s$"
    return re.sub(pattern, " ]", string)

def pickTheNextDesign(path):
    css_files = os.listdir(path)
    cssToUse = 0
    with open("D:\\02_NAUKA\\STRONA-CWICZENIA-FRANCUSKIE\\VERIFIED_2022-10-10_2\\automatyzacja-python\\cssUsed.txt") as cssMemory:
        lastCssUsed = int(cssMemory.read())
    print("lastCssUsed --", lastCssUsed)
    print("len(css_files) --", len(css_files))
    if lastCssUsed + 1 < len(css_files):
        cssToUse = lastCssUsed + 1    
    else:
        cssToUse = 0
    
    with open("D:\\02_NAUKA\\STRONA-CWICZENIA-FRANCUSKIE\\VERIFIED_2022-10-10_2\\automatyzacja-python\\cssUsed.txt", "w") as cssMemory:
        cssMemory.write(str(cssToUse))
    
    print("cssToUse -- ", cssToUse)
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
            with open('automatyzacja-python\\exerciceNumber.txt') as numRepoRead:
                exNumber = int(numRepoRead.read()) + 1

            #create the target folder
            tgtDirectoryName = "missing-element-cw" + str(exNumber)
            os.mkdir(tgtDirectoryName)
            parentDirectory = os.path.abspath(os.getcwd())
            #copy files from src folder to tgt folder
            cptr(os.path.join(parentDirectory, 'missing-element'), tgtDirectoryName)
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
            with open('automatyzacja-python\\exerciceNumber.txt', 'w') as numRepoWrite:
                numRepoWrite.write(str(exNumber))
        if file.find("pytanie-odpowiedz") > -1:
            df = pd.read_csv(os.path.join(hot_folder, file),
                 delimiter=';',
                 encoding='utf-8',
                 header=0) 
            
            questionsString = "questions = [ "
            answersString = "answers = [ "
            hintsString = "hints = [ "

            for array in df.values:
                questionsString = questionsString + f'"{array[0]}", '
                answersString = answersString + f'"{array[1]}", '
                hintsString = hintsString + f'"{array[2]}", '

            questionsString = finishJSArrayString(questionsString)
            answersString = finishJSArrayString(answersString)
            hintsString = finishJSArrayString(hintsString)

            print(questionsString)
            print(answersString)
            print(hintsString)

                        #check the exercice number
            with open('automatyzacja-python\\exerciceNumber.txt') as numRepoRead:
                exNumber = int(numRepoRead.read()) + 1

            #create the target folder
            tgtDirectoryName = "pytanie-odpowiedz-cw" + str(exNumber)
            os.mkdir(tgtDirectoryName)
            parentDirectory = os.path.abspath(os.getcwd())
            #copy files from src folder to tgt folder
            cptr(os.path.join(parentDirectory, 'pytanie-odpowiedz'), tgtDirectoryName)

            #modify the missing-element.js
            with open(os.path.join(tgtDirectoryName, "pytanie-odpowiedz.js"), 'r', encoding='utf-8') as jsf:
                content = jsf.read()
                content = content.replace("questions = []", questionsString)
                content = content.replace("answers = []", answersString)
                content = content.replace("hints = []", hintsString)

            with open(os.path.join(tgtDirectoryName, "missing-element.js"), 'w', encoding='utf-8') as jsfw:
                 jsfw.write(content)
                           
            #write exercice number
            with open('automatyzacja-python\\exerciceNumber.txt', 'w') as numRepoWrite:
                numRepoWrite.write(str(exNumber))


#Picking the name of the css file to be used in this exercice
cssToBeUsed = pickTheNextDesign(r"D:\02_NAUKA\STRONA-CWICZENIA-FRANCUSKIE\VERIFIED_2022-10-10_2\missing-element\dist")
cssHrefString = f'href="{cssToBeUsed}"'

#Writing the reference to the css file in the index.html
with open(os.path.join(tgtDirectoryName, 'index.html'), 'r', encoding='utf-8') as indexHtmlr:
    content = indexHtmlr.read()
    content = content.replace('href="<css-to-be-used>"', cssHrefString)

with open(os.path.join(tgtDirectoryName, 'index.html'), 'w', encoding='utf-8') as indexHtmlw:
    indexHtmlw.write(content)

#creating the list of css files to then delete those that are not used in the index.html
distFiles = os.listdir(os.path.join(tgtDirectoryName, "dist"))

for file in distFiles:
    if "dist\\" + file != cssToBeUsed:
        os.remove(os.path.join(tgtDirectoryName, "dist", file))
        print(f"{file} has been deleted")
    else:
        print(f"{file} IS KEPT")

print("Done!")