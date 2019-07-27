import numpy as np
import glob
import os

# Collect files
path = r'./data/Scripts - TNG/*.txt'
all_files = glob.glob(path)

# Sort files
indices = np.argsort([int(os.path.basename(f)[:-4]) for f in all_files])
all_files = np.asarray(all_files)[indices]

picard_script = []
dialog_chunk = ''
recording = False
for f in all_files:
    script = np.genfromtxt(f, dtype=str, delimiter='\n', encoding='latin1')
    for line in script:
        # Picard dialog always begins with 'PICARD'
        if 'PICARD' in line:
            recording = True
            continue  # Skip line only containing Picard's name
        if recording:
            # Dialog lines always begin with three '\t' characters and occur immediately after character name line
            if line.count('\t') == 3:
                line = line.strip('\t')
                dialog_chunk += ' {}'.format(line)
            else:
                if '?' in dialog_chunk:
                    picard_script.append(dialog_chunk[1:])
                dialog_chunk = ''
                recording = False




