import pandas as pd

# Read entire CSV file into a DataFrame
df = pd.read_csv("D:\\02_NAUKA\\STRONA-CWICZENIA-FRANCUSKIE\\VERIFIED_2022-10-10_2\\missing-element-cw2\\cw2.csv",
                 delimiter=';',
                 encoding='utf-8',
                 header=0)

'''
print(df.columns)
print(df.index)
print(df.values[0])
'''

firstPart = []
secondPart = []
missingElement = []
hints = []

for array in df.values:
    firstPart.append(array[0])
    secondPart.append(array[1])
    missingElement.append(array[2])
    hints.append(array[3])

print("first part:", firstPart)
print("second part:", secondPart)
print("missing element:", missingElement)
print("hints:", hints)

# Access specific columns
#print(df['column_name'])

'''
# Additional options
df = pd.read_csv('your_file.csv', 
    delimiter=';',  # if not comma-separated
    encoding='utf-8',  # specify encoding
    header=0  # use first row as column names
)

'''
