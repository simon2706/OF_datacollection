# -*- coding: utf-8 -*-

import pandas as pd
import os
import json


def get_all_tasks_timestamps(path):
    timestamps = pd.read_csv(path)
    timestamps = timestamps[['Participant', 'TaskA_timestamp',
                             'TaskA_startVideo_timestamp',
                             'TaskB_timestamp', 'TaskB_startVideo_timestamp',
                             'TaskC_timestamp', 'TaskC_startVideo_timestamp',
                             'TaskD_timestamp', 'TaskD_startVideo_timestamp']]
    timestamps = timestamps.dropna()
    return timestamps


def get_maxMagnitude_frames(path):
    frames = pd.read_csv(path)
    frames = frames[['Participant', 'TaskA', 'TaskB', 'TaskC', 'TaskD']]
    frames = frames.dropna()
    return frames


def get_frame(frames, subject, task):
    return frames.loc[frames.Participant == subject][task].iloc[0]


def fix_timestamp(timestamps, subject, task, timestamp):
    videoStart = timestamps.loc[timestamps.Participant == subject][task + '_startVideo_timestamp'].iloc[0]
    if videoStart[-1] == "'":
        videoStart = float(videoStart[:-1])
    new_timestamp = videoStart + (timestamp - videoStart) / 1.5
    return new_timestamp


def get_timestamp(timestamps, subject, task):
    timestamp = timestamps.loc[timestamps.Participant == subject][task + '_timestamp'].iloc[0]
    if timestamp[-1] == "'":
        timestamp = timestamp[:-1]
    timestamp = float(timestamp)
    timestamp = fix_timestamp(timestamps, subject, task, timestamp)
    return timestamp


def generate_new_time_column(df, frame, timestamp):
    df = df.loc[df['Frame#'] >= int(frame)]
    df.loc[df['Frame#'] == int(frame), 'Time_corrected'] = timestamp
    s = (df.Time_corrected.isna().cumsum() * 0.001)
    df['Time_corrected'] = df['Time_corrected'].fillna(method='ffill')
    df['Time_corrected'] = df['Time_corrected'].astype('float') + s
    return df


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


def get_task_timestamps_from_json(path_to_data, subject, task, filename):
    with open(path_to_data + os.sep + subject + os.sep + task + os.sep + filename) as f:
        data = json.load(f)
    f.close()

    calibration_start_timestamp = [
       element['Timestamp'] / 1000 + 946684800 for element in data if 'calibration' in element['Label']][0]
    calibration_end_timestamp = [
       element['Timestamp'] / 1000 + 946684800 for element in data if 'calibration' in element['Label']][-1]

    df_timestamps = pd.DataFrame(columns=['start', 'end'])
    df_timestamps = df_timestamps.append({'start': calibration_start_timestamp,
                                          'end': calibration_end_timestamp + 1.5},  # adding 1.5-second data from the end of last expression
                                         ignore_index=True)
    return df_timestamps


def save_files(df, subject, task, task_timestamps, path_to_saved_files, filename=""):
    for i in range(task_timestamps.shape[0]):
        start = task_timestamps.iloc[i, 0]
        end = task_timestamps.iloc[i, 1]
        df_task = df.loc[(df.Time_corrected >= start) & (df.Time_corrected <= end)]

        if not os.path.exists(path_to_saved_files + os.sep + subject):
            os.mkdir(path_to_saved_files + os.sep + subject)
        if not os.path.exists(path_to_saved_files + os.sep + subject + os.sep +
                              task):
            os.mkdir(path_to_saved_files + os.sep + subject + os.sep + task)

        if filename != "":
            df_task.to_csv(path_to_saved_files + os.sep + subject + os.sep +
                           task + os.sep + filename + '.csv', index=False)
            return
        df_task.to_csv(path_to_saved_files + os.sep + subject + os.sep + task +
                       os.sep + task + '_' + str(i + 1) + '.csv', index=False)
