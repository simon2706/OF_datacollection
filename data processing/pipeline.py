# -*- coding: utf-8 -*-

from libs.load_data import load_data
import numpy as np

# insert path/name of the csv file
path_to_csv = r"C:\Users\kipri\OneDrive\Documents\EmteqLabs\EmteqVR Open Face System\Upload\Participant 01\TaskB\2022-04-28T12-52-04.csv"

df = load_data(path_to_csv)

# calculate accelerometer magnitude signal
df['accelerometer_magnitude'] = np.sqrt(np.square(df['Imu/Accelerometer.x']) +
                                        np.square(df['Imu/Accelerometer.y']) +
                                        np.square(df['Imu/Accelerometer.z']))

# plot accelerometer magnitude signal
df['accelerometer_magnitude'].plot(figsize=(20, 5))

# if you need to zoom in on the signal, use .iloc
df['accelerometer_magnitude'].iloc[0:100000].plot(figsize=(15, 3))

# find maximum peak in the accelerometer magnitude signal
max_acc_mag = df['accelerometer_magnitude'].iloc[0:100000].max()

# find the Frame# corresponding to the maximum peak
frame = df.loc[df['accelerometer_magnitude'] == max_acc_mag]['Frame#'].iloc[0]
