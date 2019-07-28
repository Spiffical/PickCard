import numpy as np
import glob
import os

import datamodel

def breakApartDialog(script, character):
    scipt_exract = []
    dialog_chunk = ''
    recording = False

    for line in script:
        if character in line:
            recording = True
            data = datamodel.datamodel.copy()
            data["type"] = "dialog"
            data["character"] = character
            continue  # Skip line only containing character name
        if recording:
            # Dialog lines always begin with three '\t' characters and occur immediately after character name line
            if line.count('\t') == 3:
                line = line.strip('\t')
                dialog_chunk += ' {}'.format(line)
            else:
                data["body"] = dialog_chunk
                scipt_exract.append(data)
                dialog_chunk = ''
                recording = False
    return scipt_exract

def splitDialogByType(dialog, delimiter="?"):
    output = []
    for elem in dialog:
        if delimiter in elem["body"]:
            output.append(elem)
    return output

# Collect files
path = r'./data/Scripts - TNG/*.txt'
all_files = glob.glob(path)

# Sort files
indices = np.argsort([int(os.path.basename(f)[:-4]) for f in all_files])
all_files = np.asarray(all_files)[indices]
all_dialog = []
for f in all_files:
    script = np.genfromtxt(f, dtype=str, delimiter='\n', encoding='latin1')
    for character in datamodel.characters:
        all_dialog += breakApartDialog(script, character)

picard = [x for x in all_dialog if x['character'] is 'PICARD']
data = [x for x in all_dialog if x['character'] is 'DATA']

picard_questions = splitDialogByType(picard, delimiter="?")

