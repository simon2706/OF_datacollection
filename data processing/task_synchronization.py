# -*- coding: utf-8 -*-

import os
from libs.load_data import load_data
from libs.sync_utils import *

import warnings
warnings.filterwarnings('ignore')

subjects_new_dls = ['Participant 15', 'Participant 16', 'Participant 17',
                    'Participant 18', 'Participant 19', 'Participant 20',
                    'Participant 21', 'Participant 22', 'Participant 23',
                    'Participant 24', 'Participant 25', 'Participant 26',
                    'Participant 27', 'Participant 28', 'Participant 29',
                    'Participant 30']

timestamps = get_all_tasks_timestamps(r'timestamps.csv')
frames = get_maxMagnitude_frames(r'maxMagnitude.csv')

path_to_data = r"Data"
path_to_saved_files = r"Data_processed"

for subject in os.lsitdir('Data'):
    print(subject)
    for task in os.listdir(path_to_data + os.sep + subject):
        print(task)
        for file in os.listdir(path_to_data + os.sep + subject + os.sep + task):
            if 'csv' in file and 'AV_scores' not in file:
                print(file)

                df = load_data(path_to_data + os.sep + subject + os.sep + task + os.sep + file)

                frame = get_frame(frames, subject, task)
                timestamp = get_timestamp(timestamps, subject, task)

                df = generate_new_time_column(df, frame, timestamp)
                
                # The subjects that are recorded with the new dls have correct
                # timestamps in the csv, so no need of using the corrected
                # values from the synchronization
                if subject in subjects_new_dls:
                    df['Time_corrected'] = df['Time']

                if task == 'TaskA':
                    filename = str(int(subject.split()[1])) + '_TaskA_timestamps.txt'
                    task_timestamps = get_task_timestamps(path_to_data, subject,
                                                          task, filename)
                    save_files(df, subject, task, task_timestamps, path_to_saved_files)

                if task == 'TaskB':
                    filename = str(int(subject.split()[1])) + '_TaskB_timestamps.txt'
                    task_timestamps = get_task_timestamps(path_to_data, subject,
                                                          task, filename)
                    save_files(df, subject, task, task_timestamps, path_to_saved_files)

                if task == 'TaskC':
                    filename = 'timestamps.txt'
                    task_timestamps = get_task_timestamps(path_to_data, subject,
                                                          task, filename)
                    task_timestamps.iloc[0, 1] = task_timestamps.iloc[-1, 1]
                    task_timestamps = task_timestamps.iloc[:1, :]
                    save_files(df, subject, task, task_timestamps, path_to_saved_files,
                               'videos')
                    
                    filename = 'baseline_timestamps.txt'
                    task_timestamps = get_task_timestamps(path_to_data, subject,
                                                          task, filename)
                    save_files(df, subject, task, task_timestamps, path_to_saved_files,
                               'baseline')
                    
                    filename = file.split('.')[0] + '.json'
                    print(filename)
                    task_timestamps = get_task_timestamps_from_json(path_to_data,
                                                                    subject,
                                                                    task,
                                                                    filename)
                    save_files(df, subject, task, task_timestamps,
                               path_to_saved_files,
                               'calibration')
                    
                if task == 'TaskD':
                    filename = 'article_timestamps.txt'
                    task_timestamps = get_task_timestamps(path_to_data, subject,
                                                          task, filename)
                    save_files(df, subject, task, task_timestamps,
                               path_to_saved_files, 'speaking')
