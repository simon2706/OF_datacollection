import os
import random
import pandas as pd
import time

from playVideo import play_video


def get_input():
    values = list()

    while True:
        #arousal = simpledialog.askinteger("Input","Value for arousal from 1 to 9: ")
        arousal = input('Value for arousal from 1 to 9: ')
        if arousal.isdigit():
            arousal = int(arousal)
            if arousal in range(1,10):
                values.append(arousal)
                break
            print('Wrong value')
        else:
            print('Number is not entered')


    while True:
        #valence = simpledialog.askinteger("Input","Value for valence from 1 to 9: ")
        valence = input('Value for alence from 1 to 9: ')
        if valence.isdigit():
            valence = int(valence)
            if valence in range(1,10):
                values.append(valence)
                break
            print('Wrong value')
        else:
            print('Number is not entered !')
        
    return values


def get_subfolders(path_to_data):
    video_categories = os.listdir(path_to_data)
    random.shuffle(video_categories)
    print(video_categories)
    return video_categories


def work_folders(path_to_data, subfolders):
    av_scores = pd.DataFrame()

    for folder in subfolders:
        for file in os.listdir(path_to_data+os.sep+folder):

            path_to_video = path_to_data+os.sep+folder+os.sep+file

            play_video(path_to_video, 'timestamps.txt')

            values = get_input()
            print(values)
            time.sleep(5)
            temp = pd.DataFrame([[path_to_video, values[0], values[1]]],
                                columns=['path_to_video','arousal', 'valence'])
            av_scores = pd.concat([av_scores, temp])

    return av_scores


if __name__ == "__main__":
    path_to_data = r"C:\Users\kipri\OneDrive\Desktop\OpenFace Data Collection\TaskC"
    av_scores = work_folders(path_to_data, get_subfolders(path_to_data))
    av_scores.to_csv("AV_scores.csv", index=False)
