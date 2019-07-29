import numpy as np
import glob
import os

datamodel = {
    "type": None,
    "character": None,
    "paranthetical": None,
    "start_line": None,
    "end_line": None,
    "body": None
}

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
    
    # setup state machine
    state = None # "title" | "action" | "dialogue"
    action_accumilator = ""

    try:
        index = 0
        while index < len(script):
            line = script[index]
            # check if "scene"
            if line[0].isdigit():
                data = datamodel.copy()
                data['filename'] = f
                data['type'] = "scene"
                data['start_line'] = index
                data['end_line'] = index
                data['body'] = line[5:]
                all_dialog.append(data)
                index += 1
            # check if "action"
            elif line.count("\t") is 1:
                data = datamodel.copy()
                data['filename'] = f
                data['type'] = "action"
                data['start_line'] = index
                data['body'] = line.strip("\t")
                while script[index + 1].count("\t") is 1:
                    data['body'] += " {0}".format(script[index + 1].strip("\t"))
                    index += 1
                data['end_line'] = index
                all_dialog.append(data)
                index += 1
            # check if "dialogue"
            elif line.count("\t") is 5:
                data = datamodel.copy()
                data['filename'] = f
                data['type'] = "dialog"
                data['start_line'] = index
                data['character'] = line.strip("\t")
                data['body'] = ""
                while script[index + 1].count("\t") > 2 and script[index + 1].count("\t") < 5 :
                    if "(" and ")" in script[index + 1]:
                        data['paranthetical'] = script[index + 1].strip("\t")
                        index += 1
                    else:
                        data['body'] += " {0}".format(script[index + 1].strip("\t"))
                        index += 1
                data['body'] = data['body'][1:]
                data['end_line'] = index
                all_dialog.append(data)
                index += 1
            else:
                index += 1

    except IndexError:
        pass


picard_dialog = [x for x in all_dialog if x['character'] == "PICARD"]
data_dialog = [x for x in all_dialog if x['character'] == "DATA"]

picard_questions = splitDialogByType(picard_dialog, delimiter="?")
engage = [x for x in picard_dialog if "engage" in x['body'].lower()]