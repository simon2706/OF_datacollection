import os
import random
from csv import writer

from play_video import play_video


def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)


def get_input():
    values = list()

    while True:
        arousal = int(input('Value for arousal from 1 to 9: '))
        if arousal in range(1, 9):
            values.append(arousal)
            break
        print('Wrong value')

    while True:
        valence = int(input('Value for valence from 1 to 9: '))
        if valence in range(1, 9):
            values.append(valence)
            break
        print('Wrong value')

    return values


def get_dir_specific(path):
    os.chdir(path)
    directories = os.listdir()
    for el in directories:
        if el == 'TaskC':
            print('TaskC folder exists')
            os.chdir(path + os.sep + el)
            break
        else:
            print('TaskC folder not found in ' + path)
            exit()


def get_subfolders():
    subfolders = [x[0] for x in os.walk(os.getcwd())][1:]
    random.shuffle(subfolders)
    print(subfolders)
    return subfolders


def work_folders(subfolders):
    for folder in subfolders:
        os.chdir(folder)
        print(os.getcwd())
        for file in os.listdir():
            play_video(file, 'timestamps.txt')
            values = get_input()
            print(values)
            path = os.getcwd() + os.sep + file
            row_content = [path, values[0], values[1]]
            append_list_as_row('TaskC_data.csv', row_content)
            print(path)
        os.chdir('..')


if __name__ == "__main__":
    print(os.getcwd())
    get_dir_specific(os.getcwd())
    work_folders(get_subfolders())
