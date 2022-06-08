# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 14:15:06 2021

@author: ivana
"""

import json
import os
import pandas as pd

task = 'TaskA_1'  # choose one from TaskA_1, TaskA_2, TaskA_3, TaskA_4, TaskB_1, TaskB_2, TaskB_3, TaskB_4

f = open(task + '.json',)
data = json.load(f)
f.close()
subjects = os.listdir('D:/Data_Praksa/Data_processed')

for i in range(len(subjects)):
    subject_data = data[i]
    subject_data_labels = subject_data['label']

    df_labels = pd.DataFrame()
    for j in range(len(subject_data_labels)):
        df = pd.DataFrame()

        df['label'] = subject_data_labels[j]['timeserieslabels']
        df['start'] = subject_data_labels[j]['start']
        df['end'] = subject_data_labels[j]['end']

        df_labels = df_labels.append(df)

        sub = subject_data['csv_url'].split('-')[1][:14]
    print(sub)
    df_labels.to_csv(r'Labels_JSON' + os.sep + sub + '_' + task + '.csv',
                     index=False)

for subject in subjects:
    print(subject)
    data = pd.read_csv("Data_processed" + os.sep + subject + os.sep +
                       task.split('_')[0] + os.sep + task + ".csv")
    data.reset_index(inplace=True, drop=False)
    events = pd.read_csv("Labels_JSON" + os.sep + subject.split(' ')[0] +
                         '_' + subject.split(' ')[1] + "_" + task + ".csv")

    for idx, event in enumerate(events.iloc[:, 0]):
        data.loc[(data.index >= events.iloc[idx, 1]) &
                 (data.index <= events.iloc[idx, 2]), 'event'] = event

    if not os.path.exists("Data_processed_labelled" + os.sep + subject):
        os.mkdir("Data_processed_labelled" + os.sep + subject)
    if not os.path.exists("Data_processed_labelled" + os.sep + subject +
                          os.sep + task.split('_')[0]):
        os.mkdir("Data_processed_labelled" + os.sep + subject + os.sep +
                 task.split('_')[0])
    data.to_csv("Data_processed_labelled" + os.sep + subject + os.sep +
                task.split('_')[0] + os.sep + task + ".csv",
                index=False)
