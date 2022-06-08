# -*- coding: utf-8 -*-
"""
Created on Thu May 26 00:08:44 2022

@author: user
"""
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')


def get_video_names(path_to_data, subject, task, filename):
    videos = pd.read_csv(path_to_data + os.sep + subject +
                         os.sep + task + os.sep + filename, header=None)
    videos = videos.loc[0::2, :]
    videos = videos.iloc[:, 0].str.slice(-13, -4)
    return videos


def get_task_timestamps(path_to_data, subject, task, filename):
    timestamps = pd.read_csv(path_to_data + os.sep + subject +
                             os.sep + task + os.sep + filename, header=None)
    timestamps = timestamps[0].str.split(';', expand=True)

    df_timestamps = pd.DataFrame(columns=['start', 'end'])
    for i in range(1, timestamps.shape[0], 2):
        df_timestamps = df_timestamps.append({'start': float(timestamps.iloc[i, 0].split()[1]),
                                              'end': float(timestamps.iloc[i, 1].split()[1])},
                                             ignore_index=True)
    return df_timestamps


path_to_data = r"Data"
path_to_saved_files = r"Data_processed_labelled"

for subject in os.listdir("Data_processed"):
    print(subject)
    df = pd.read_csv('Data_processed' + os.sep + subject + os.sep + 'TaskC' + os.sep + 'videos.csv')
    filename = 'timestamps.txt'
    task_timestamps = get_task_timestamps(path_to_data, subject, 'TaskC',
                                          filename)
    task_timestamps['video'] = get_video_names(path_to_data, subject, 'TaskC',
                                               filename).reset_index(drop=True)

    for i in range(task_timestamps.shape[0]):
        df.loc[(df['Time_corrected'] >= task_timestamps.iloc[i, 0]) &
               (df['Time_corrected'] <= task_timestamps.iloc[i, 1]),
               'video'] = task_timestamps.iloc[i, 2]

    ratings = pd.read_csv('Data' + os.sep + subject + os.sep + 'TaskC' +
                          os.sep + 'AV_scores.csv')
    ratings['path_to_video'] = ratings['path_to_video'].str.slice(-13, -4)
    ratings.columns = ['video', 'arousal', 'valence']

    df = df.merge(ratings, on='video', how='left')

    df = df[['Frame#', 'Time',
             'Emg/Contact[2]', 'Emg/Raw[2]',
             'Emg/Filtered[2]', 'Emg/Amplitude[2]',
             'Emg/Contact[1]', 'Emg/Raw[1]', 'Emg/Filtered[1]',
             'Emg/Amplitude[1]', 'Emg/Contact[0]',
             'Emg/Raw[0]', 'Emg/Filtered[0]', 'Emg/Amplitude[0]',
             'Emg/Contact[3]', 'Emg/Raw[3]',
             'Emg/Filtered[3]', 'Emg/Amplitude[3]',
             'Emg/Contact[6]', 'Emg/Raw[6]', 'Emg/Filtered[6]',
             'Emg/Amplitude[6]', 'Emg/Contact[5]',
             'Emg/Raw[5]', 'Emg/Filtered[5]', 'Emg/Amplitude[5]',
             'Emg/Contact[4]', 'Emg/Raw[4]',
             'Emg/Filtered[4]', 'Emg/Amplitude[4]', 'HeartRate/Average',
             'Ppg/Raw.ppg', 'Ppg/Raw.proximity', 'Imu/Accelerometer.x',
             'Imu/Accelerometer.y', 'Imu/Accelerometer.z', 'Magnetometer/Raw.x',
             'Magnetometer/Raw.y', 'Magnetometer/Raw.z', 'Gyroscope/Raw.x',
             'Gyroscope/Raw.y', 'Gyroscope/Raw.z', 'Pressure/Raw',
             'Time_corrected', 'video', 'arousal', 'valence']]

    df.columns = ['Frame#', 'Time',
                  'Emg/Contact[2]', 'Emg/Raw[2]',
                  'Emg/Filtered[2]', 'Emg/Amplitude[2]',
                  'Emg/Contact[1]', 'Emg/Raw[1]', 'Emg/Filtered[1]',
                  'Emg/Amplitude[1]', 'Emg/Contact[0]',
                  'Emg/Raw[0]', 'Emg/Filtered[0]', 'Emg/Amplitude[0]',
                  'Emg/Contact[3]', 'Emg/Raw[3]',
                  'Emg/Filtered[3]', 'Emg/Amplitude[3]',
                  'Emg/Contact[6]', 'Emg/Raw[6]', 'Emg/Filtered[6]',
                  'Emg/Amplitude[6]', 'Emg/Contact[5]',
                  'Emg/Raw[5]', 'Emg/Filtered[5]', 'Emg/Amplitude[5]',
                  'Emg/Contact[4]', 'Emg/Raw[4]',
                  'Emg/Filtered[4]', 'Emg/Amplitude[4]', 'HeartRate/Average',
                  'Ppg/Raw.ppg', 'Ppg/Raw.proximity', 'Accelerometer/Raw.x',
                  'Accelerometer/Raw.y', 'Accelerometer/Raw.z', 'Magnetometer/Raw.x',
                  'Magnetometer/Raw.y', 'Magnetometer/Raw.z', 'Gyroscope/Raw.x',
                  'Gyroscope/Raw.y', 'Gyroscope/Raw.z', 'Pressure/Raw', 'Time_corrected',
                  'video', 'arousal', 'valence']

    if not os.path.exists('Data_processed_labelled' + os.sep + subject):
        os.mkdir('Data_processed_labelled' + os.sep + subject)
    if not os.path.exists('Data_processed_labelled' + os.sep + subject + os.sep + 'TaskC'):
        os.mkdir('Data_processed_labelled' + os.sep + subject + os.sep + 'TaskC')
    df.to_csv('Data_processed_labelled' + os.sep + subject + os.sep + 'TaskC' + os.sep + 'videos.csv')
