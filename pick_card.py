import numpy as np
import glob

path = r'/Users/spencerbialek/Documents/tng-transcripts/Scripts - TNG/*.txt'
all_files = glob.iglob(path)

picard_script = []
start_recording = False
for f in all_files:
    script = np.genfromtxt(f, dtype=str, delimiter='\n')
    for line in script:
        if 'picard' in line.lower():

            picard_script.append(line)

