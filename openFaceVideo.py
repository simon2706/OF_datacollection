import os
import sys
import random
import pandas as pd

from pathlib import Path
path = Path(os.path.abspath(""))
sys.path.append(str(path))

from play_video import play_video
from csv import writer


def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

a = 1
# how to get subfolder of current folder
TaskC = os.path.dirname('.\\TaskC')
p = os.getcwd()
print(p)
os.chdir(p+os.sep+'TaskC')
p1 = p + os.sep + 'TaskC'
# how to get all subfolders of current folder
TaskC_subfolders = [x[0] for x in os.walk(TaskC)][1:]
random.shuffle(TaskC_subfolders)
print(TaskC_subfolders)
append_list_as_row(p1+'/TaskC_data.csv',['path','arousal','valence'])
for folder in TaskC_subfolders:
    os.chdir(folder)
    print(os.getcwd())
    for file in os.listdir():
        play_video(file, 'timestamps.txt')
        #check if is not 1-9 number
        while True:
            arousal = int(input('Value for arousal from 1 to 9: '))
            if arousal in range(1,9):
                break
        while True:
            valence = int(input('Value for valence from 1 to 9: '))
            if valence in range(1,9):
                break
        path = os.getcwd() + '/' + file
        row_content = [path, arousal, valence]
        append_list_as_row(p1+'/TaskC_data.csv', row_content)
        print(path)
    os.chdir('..')
    #print(os.getcwd())
