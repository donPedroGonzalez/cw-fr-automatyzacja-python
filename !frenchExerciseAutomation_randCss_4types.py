import re
import os
import stat
import pandas as pd
from distutils.dir_util import copy_tree as cptr
from distutils.dir_util import remove_tree as rmtr
#import fileinput

# Configuration paths - update these to match your structure
hot_folder = "D:\\02_NAUKA\\STRONA-CWICZENIA-FRANCUSKIE\\VERIFIED_2022-10-10_2\\matching-exercise\\hot_folder"
css_path = "D:\\02_NAUKA\\STRONA-CWICZENIA-FRANCUSKIE\\VERIFIED_2022-10-10_2\\matching-exercise\\dist"

#hot_folder = "D:\\02_NAUKA\\STRONA-CWICZENIA-FRANCUSKIE\\VERIFIED_2022-10-10_2\\missing-element\\hot_folder"
#css_path = "D:\\02_NAUKA\\STRONA-CWICZENIA-FRANCUSKIE\\VERIFIED_2022-10-10_2\\missing-element\\dist"

#hot_folder = "D:\\02_NAUKA\\STRONA-CWICZENIA-FRANCUSKIE\\VERIFIED_2022-10-10_2\\pytanie-odpowiedz\\hot_folder"
#css_path = "D:\\02_NAUKA\\STRONA-CWICZENIA-FRANCUSKIE\\VERIFIED_2022-10-10_2\\pytanie-odpowiedz\\dist"

#hot_folder = "D:\\02_NAUKA\\STRONA-CWICZENIA-FRANCUSKIE\\VERIFIED_2022-10-10_2\\word-order\\hot_folder"
#css_path = "D:\\02_NAUKA\\STRONA-CWICZENIA-FRANCUSKIE\\VERIFIED_2022-10-10_2\\word-order\\dist"

tgtDirectoryName = parentDirectory = ""

# Working methods
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

def deleteProtectedDirectory(dir_path):
    # Changing file permissions
    for root, dirs, files in os.walk(dir_path):
        for dir in dirs:
            os.chmod(os.path.join(root, dir), stat.S_IRWXU)
        for file in files:
            os.chmod(os.path.join(root, file), stat.S_IRWXU)
    # Removing the directory
    rmtr(dir_path)

def createJSObjectArray(data_list):
    """Helper function to create JavaScript object array strings"""
    result = "[\n"
    for i, item in enumerate(data_list):
        result += "        " + item
        if i < len(data_list) - 1:
            result += ",\n"
    result += "\n    ]"
    return result

# The csv file to be processed should have a specific file name structure and should be utf-8 encoded.
# <exercice-type>_otherContent.csv

hf_files = os.listdir(hot_folder)
print(hf_files)

for file in hf_files:
    if file.endswith('csv'):
        # MISSING-ELEMENT EXERCISE TYPE
        if file.find("missing-element") > -1:
            df = pd.read_csv(os.path.join(hot_folder, file),
                 delimiter=';',
                 encoding='utf-8',
                 header=0) 
            
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

            # Check the exercice number
            with open('automatyzacja-python\\exerciceNumber.txt') as numRepoRead:
                exNumber = int(numRepoRead.read()) + 1

            # Create the target folder
            tgtDirectoryName = "missing-element-cw" + str(exNumber)
            os.mkdir(tgtDirectoryName)
            parentDirectory = os.path.abspath(os.getcwd())
            # Copy files from src folder to tgt folder
            cptr(os.path.join(parentDirectory, 'missing-element'), tgtDirectoryName)
            # Deleting the .git directory of the parent folder and all of its content from the newly created exercice folder
            git_path = os.path.join(tgtDirectoryName, ".git")
            if os.path.exists(git_path):
                deleteProtectedDirectory(git_path)
            vs_path = os.path.join(tgtDirectoryName, ".vs")
            if os.path.exists(vs_path):
                deleteProtectedDirectory(vs_path)
            vs_code_path = os.path.join(tgtDirectoryName, ".vscode")
            if os.path.exists(vs_code_path):
                deleteProtectedDirectory(vs_code_path)

            # Modify the missing-element.js
            with open(os.path.join(tgtDirectoryName, "missing-element.js"), 'r', encoding='utf-8') as jsf:
                content = jsf.read()
                content = content.replace("firstPart = []", firstPartString)
                content = content.replace("secondPart = []", secondPartString)
                content = content.replace("missingElement = []", missingElementString)
                content = content.replace("hints = []", hintsString)

            with open(os.path.join(tgtDirectoryName, "missing-element.js"), 'w', encoding='utf-8') as jsfw:
                 jsfw.write(content)
                           
            # Write exercice number
            with open('automatyzacja-python\\exerciceNumber.txt', 'w') as numRepoWrite:
                numRepoWrite.write(str(exNumber))
        
        # PYTANIE-ODPOWIEDZ EXERCISE TYPE
        elif file.find("pytanie-odpowiedz") > -1:
            df = pd.read_csv(os.path.join(hot_folder, file),
                 delimiter=';',
                 encoding='utf-8',
                 header=0) 
            
            questionsString = "questions = [ "
            answersString = "answers = [ "
            hintsString = "hints = [ "

            for array in df.values:
                questionsString = questionsString + f"'{array[0]}', "
                answersString = answersString + f"'{array[1]}', "
                hintsString = hintsString + f"'{array[2]}', "

            questionsString = finishJSArrayString(questionsString)
            answersString = finishJSArrayString(answersString)
            hintsString = finishJSArrayString(hintsString)

            print(questionsString)
            print(answersString)
            print(hintsString)

            # Check the exercice number
            with open('automatyzacja-python\\exerciceNumber.txt') as numRepoRead:
                exNumber = int(numRepoRead.read()) + 1

            # Create the target folder
            tgtDirectoryName = "pytanie-odpowiedz-cw" + str(exNumber)
            os.mkdir(tgtDirectoryName)
            parentDirectory = os.path.abspath(os.getcwd())
            # Copy files from src folder to tgt folder
            cptr(os.path.join(parentDirectory, 'pytanie-odpowiedz'), tgtDirectoryName)
            # Deleting the .git directory of the parent folder and all of its content from the newly created exercice folder
            git_path = os.path.join(tgtDirectoryName, ".git")
            if os.path.exists(git_path):
                deleteProtectedDirectory(git_path)

            # Modify the pytanie-odpowiedz.js
            with open(os.path.join(tgtDirectoryName, "pytanie-odpowiedz.js"), 'r', encoding='utf-8') as jsf:
                content = jsf.read()
                content = content.replace("questions = []", questionsString)
                content = content.replace("answers = []", answersString)
                content = content.replace("hints = []", hintsString)

            with open(os.path.join(tgtDirectoryName, "pytanie-odpowiedz.js"), 'w', encoding='utf-8') as jsfw:
                 jsfw.write(content)
                           
            # Write exercice number
            with open('automatyzacja-python\\exerciceNumber.txt', 'w') as numRepoWrite:
                numRepoWrite.write(str(exNumber))
        
        # MATCHING EXERCISE TYPE
        elif file.find("matching-exercise") > -1:
            df = pd.read_csv(os.path.join(hot_folder, file),
                 delimiter=';',
                 encoding='utf-8',
                 header=0) 
            
            premiere_consigne_string = footer_cat_info_string  = ""            
            # Build JavaScript object array
            exerciseDataItems = []
            for index, array in enumerate(df.values):
                if index == 0:
                    # Assuming the first non-header row has: premiere_consigne;footer_cat_info
                    premiere_consigne_string = array[0]
                    footer_cat_info_string = array[1]
                else:
                    # Assuming CSV columns: french;polish
                    item = f'{{ left: "{array[0]}", right: "{array[1]}", id: {index + 1} }}'
                    exerciseDataItems.append(item)
            
            exerciseDataString = "exerciseData = " + createJSObjectArray(exerciseDataItems) + ";"
            
            print("Generated matching exercise data:")
            print(exerciseDataString)

            # Check the exercice number
            with open('automatyzacja-python\\exerciceNumber.txt') as numRepoRead:
                exNumber = int(numRepoRead.read()) + 1

            # Create the target folder
            tgtDirectoryName = "matching-exercice-cw" + str(exNumber)
            os.mkdir(tgtDirectoryName)
            parentDirectory = os.path.abspath(os.getcwd())
            # Copy files from src folder to tgt folder
            cptr(os.path.join(parentDirectory, 'matching-exercise'), tgtDirectoryName)
            
            # Clean up unnecessary directories
            for dir_name in [".git", ".vs", ".vscode"]:
                dir_path = os.path.join(tgtDirectoryName, dir_name)
                if os.path.exists(dir_path):
                    deleteProtectedDirectory(dir_path)

            # Modify the matching.js
            with open(os.path.join(tgtDirectoryName, "matching-exercise.js"), 'r', encoding='utf-8') as jsf:
                content = jsf.read()
                content = content.replace("exerciseData = []", exerciseDataString)
                content = content.replace("<premiere_consigne_string>", premiere_consigne_string)
                content = content.replace("<footer_cat_info_string>", footer_cat_info_string)

            with open(os.path.join(tgtDirectoryName, "matching-exercise.js"), 'w', encoding='utf-8') as jsfw:
                 jsfw.write(content)
                           
            # Write exercice number
            with open('automatyzacja-python\\exerciceNumber.txt', 'w') as numRepoWrite:
                numRepoWrite.write(str(exNumber))
        
        # WORD-ORDER EXERCISE TYPE
        elif file.find("word-order") > -1:
            df = pd.read_csv(os.path.join(hot_folder, file),
                 delimiter=';',
                 encoding='utf-8',
                 header=0) 
            
            # Build JavaScript object array for sentences
            sentenceItems = []
            for index, array in enumerate(df.values):
                if index == 0:
                    # Assuming the first non-header row has: premiere_consigne;footer_cat_info
                    premiere_consigne_string = array[0]
                    footer_cat_info_string = array[1]
                else:
                    # Assuming CSV columns: scrambled_words;correct_order;hint
                    # Split the scrambled and correct words by comma or space
                    scrambled_words = [f'"{word.strip()}"' for word in array[0].split('--')]
                    correct_words = [f'"{word.strip()}"' for word in array[1].split('--')]
                
                    item = f'''{{
                        scrambled: [{', '.join(scrambled_words)}],
                        correct: [{', '.join(correct_words)}],
                        hint: "{array[2]}"
                    }}'''
                    sentenceItems.append(item)
            
            sentencesString = "sentences = " + createJSObjectArray(sentenceItems) + ";"
            
            print("Generated word-order exercise data:")
            print(sentencesString)

            # Check the exercice number
            with open('automatyzacja-python\\exerciceNumber.txt') as numRepoRead:
                exNumber = int(numRepoRead.read()) + 1

            # Create the target folder
            tgtDirectoryName = "word-order-cw" + str(exNumber)
            os.mkdir(tgtDirectoryName)
            parentDirectory = os.path.abspath(os.getcwd())
            # Copy files from src folder to tgt folder
            cptr(os.path.join(parentDirectory, 'word-order'), tgtDirectoryName)
            
            # Clean up unnecessary directories
            for dir_name in [".git", ".vs", ".vscode"]:
                dir_path = os.path.join(tgtDirectoryName, dir_name)
                if os.path.exists(dir_path):
                    deleteProtectedDirectory(dir_path)

            # Modify the word-order.js
            with open(os.path.join(tgtDirectoryName, "word-order.js"), 'r', encoding='utf-8') as jsf:
                content = jsf.read()
                content = content.replace("sentences = []", sentencesString)

            with open(os.path.join(tgtDirectoryName, "word-order.js"), 'w', encoding='utf-8') as jsfw:
                 jsfw.write(content)
                           
            # Write exercice number
            with open('automatyzacja-python\\exerciceNumber.txt', 'w') as numRepoWrite:
                numRepoWrite.write(str(exNumber))

# Picking the name of the css file to be used in this exercice
cssToBeUsed = pickTheNextDesign(css_path)
cssHrefString = f'href="{cssToBeUsed}"'

# Writing the reference to the css file in the index.html
with open(os.path.join(tgtDirectoryName, 'index.html'), 'r', encoding='utf-8') as indexHtmlr:
    content = indexHtmlr.read()
    content = content.replace('href="<css-to-be-used>"', cssHrefString)

with open(os.path.join(tgtDirectoryName, 'index.html'), 'w', encoding='utf-8') as indexHtmlw:
    indexHtmlw.write(content)

# Creating the list of css files to then delete those that are not used in the index.html
distFiles = os.listdir(os.path.join(tgtDirectoryName, "dist"))

for file in distFiles:
    if "dist\\" + file != cssToBeUsed:
        os.remove(os.path.join(tgtDirectoryName, "dist", file))
        print(f"{file} has been deleted")
    else:
        print(f"{file} IS KEPT")

print("Done!")