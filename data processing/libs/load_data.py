# -*- coding: utf-8 -*-

import pandas as pd
import re
from io import StringIO


def get_metadata_info_time_offset(metadata):
    time_offset = None
    for line in metadata:
        if line.find('#Time/Seconds.referenceOffset') != -1:
            time_offset = float(line.split(',')[1])
    return time_offset


def get_metadata_info_acceleration_divisor(metadata):
    acceleration_divisor = None
    for line in metadata:
        if line.find('#Imu/Properties.accelerationDivisor') != -1 or line.find('#Accelerometer/Properties.rawDivisor') != -1:
            acceleration_divisor = float(line.split(',')[1])
    return acceleration_divisor


def get_metadata_info_gyroscope_divisor(metadata):
    gyroscope_divisor = None
    for line in metadata:
        if line.find('#Imu/Properties.gyroscopeDivisor') != -1 or line.find('#Gyroscope/Properties.rawDivisor') != -1:
            gyroscope_divisor = float(line.split(',')[1])
    return gyroscope_divisor


def get_metadata_info_magnetometer_divisor(metadata):
    magnetometer_divisor = None
    for line in metadata:
        if line.find('#Imu/Properties.magnetometerDivisor') != -1 or line.find('#Magnetometer/Properties.rawDivisor') != -1:
            magnetometer_divisor = float(line.split(',')[1])
    return magnetometer_divisor


def get_metadata_info_pressure_divisor(metadata):
    pressure_divisor = None
    for line in metadata:
        if line.find('#Pressure/Properties.rawDivisor') != -1:
            pressure_divisor = float(line.split(',')[1])
    return pressure_divisor


def get_metadata_info_emg_divisor(metadata):
    raw2voltage_emg_divisor = None
    for line in metadata:
        if line.find('#Emg/Properties.rawToVoltageDivisor') != -1:
            raw2voltage_emg_divisor = float(line.split(',')[1])
    return raw2voltage_emg_divisor


def get_metadata_info_contact_divisor(metadata):
    contact2impedance_divisor = None
    for line in metadata:
        if line.find('#Emg/Properties.contactToImpedanceDivisor') != -1:
            contact2impedance_divisor = float(line.split(',')[1])
    return contact2impedance_divisor


def get_metadata_info_emg_order(metadata):
    emg_order = None
    for line in metadata:
        if line.find('#Emg/Properties.ids[]') != -1:
            emg_order = line.split(',')[1:]
    return emg_order


def order_emg_columns(emg_order):
    emg_expected_order = {'RightFrontalis': 0, 'RightZygomaticus': 1,
                          'RightOrbicularis': 2, 'CenterCorrugator': 3,
                          'LeftOrbicularis': 4, 'LeftZygomaticus': 5,
                          'LeftFrontalis': 6}
    emg_columns_ordered = []
    for emg_ch in emg_order:
        emg_idx = emg_expected_order[emg_ch]
        emg_columns_ordered.append(
            ['Emg/ContactState[' + str(emg_idx) + ']',
             'Emg/Contact[' + str(emg_idx) + ']',
             'Emg/Raw[' + str(emg_idx) + ']',
             'Emg/RawLift[' + str(emg_idx) + ']',
             'Emg/Filtered[' + str(emg_idx) + ']',
             'Emg/Amplitude[' + str(emg_idx) + ']'])
    emg_columns_ordered = [
        item for sublist in emg_columns_ordered for item in sublist]
    return emg_columns_ordered


def rename_emg_cols(test_df, emg_order):
    for key in emg_order:
        test_df.columns = [
            f.replace(key, emg_order[key]) if key in f else f for f in test_df.columns]
    test_df.columns = test_df.columns.str.replace('RightOrbicularis', '2')
    test_df.columns = test_df.columns.str.replace('RightZygomaticus', '1')
    test_df.columns = test_df.columns.str.replace('RightFrontalis', '0')
    test_df.columns = test_df.columns.str.replace('CenterCorrugator', '3')
    test_df.columns = test_df.columns.str.replace('LeftFrontalis', '6')
    test_df.columns = test_df.columns.str.replace('LeftZygomaticus', '5')
    test_df.columns = test_df.columns.str.replace('LeftOrbicularis', '4')
    return test_df


def rename_accelerometer_cols(test_df):
    test_df.rename(
        {'Accelerometer/Raw.x': 'Imu/Accelerometer.x'}, axis=1, inplace=True)
    test_df.rename(
        {'Accelerometer/Raw.y': 'Imu/Accelerometer.y'}, axis=1, inplace=True)
    test_df.rename(
        {'Accelerometer/Raw.z': 'Imu/Accelerometer.z'}, axis=1, inplace=True)
    return test_df


def rename_columns(test_df, emg_columns_ordered):
    new_columns = []
    idx = 0
    for col in test_df.columns:
        if 'Emg' not in col:
            new_columns.append(col)
        else:
            new_columns.append(emg_columns_ordered[idx])
            idx = idx + 1
    test_df.columns = new_columns

    if 'Accelerometer/Raw.x' in test_df.columns:
        test_df = rename_accelerometer_cols(test_df)

    return test_df


def scale_accelerometer_data(test_df, acceleration_divisor):
    accelerometer_cols = ['Imu/Accelerometer.x',
                          'Imu/Accelerometer.y', 'Imu/Accelerometer.z']
    test_df[accelerometer_cols] = test_df[accelerometer_cols] / \
        acceleration_divisor / 9.699466695345983
    return test_df


def scale_gyroscope_data(test_df, gyroscope_divisor):
    gyroscope_cols = ['Gyroscope/Raw.x', 'Gyroscope/Raw.y',
                      'Gyroscope/Raw.z']
    test_df[gyroscope_cols] = test_df[gyroscope_cols] / gyroscope_divisor
    return test_df


def scale_magnetometer_data(test_df, magnetometer_divisor):
    magnetometer_cols = ['Magnetometer/Raw.x', 'Magnetometer/Raw.y',
                         'Magnetometer/Raw.z']
    test_df[magnetometer_cols] = test_df[magnetometer_cols] / \
        magnetometer_divisor
    return test_df


def scale_pressure_data(test_df, pressure_divisor):
    pressure_cols = ['Pressure/Raw']
    test_df[pressure_cols] = test_df[pressure_cols] / pressure_divisor
    return test_df


def scale_emg_data(test_df, raw2voltage_emg_divisor):
    emg_cols = ['Emg/Filtered[0]', 'Emg/Filtered[1]', 'Emg/Filtered[2]',
                'Emg/Filtered[3]', 'Emg/Filtered[4]', 'Emg/Filtered[5]',
                'Emg/Filtered[6]', 'Emg/Amplitude[0]', 'Emg/Amplitude[1]',
                'Emg/Amplitude[2]', 'Emg/Amplitude[3]', 'Emg/Amplitude[4]',
                'Emg/Amplitude[5]', 'Emg/Amplitude[6]']
    test_df[emg_cols] = test_df[emg_cols] / raw2voltage_emg_divisor
    return test_df


def scale_contact_data(test_df, contact2impedance_divisor):
    contact_cols = ['Emg/Contact[0]', 'Emg/Contact[1]', 'Emg/Contact[2]',
                    'Emg/Contact[3]', 'Emg/Contact[4]', 'Emg/Contact[5]',
                    'Emg/Contact[6]']
    test_df[contact_cols] = test_df[contact_cols] / contact2impedance_divisor
    return test_df


def string2dataFrame(data):
    data = re.sub(r'\n\s*\n', '\n', data, re.MULTILINE)
    data = re.sub(r'\s*\n\s*Frame#', 'Frame#', data, re.MULTILINE)
    test_df = pd.read_csv(
        StringIO(data), skip_blank_lines=True, delimiter=',', na_filter=False)
    test_df = test_df.dropna()
    return test_df


def load_data(path_to_data):
    '''
     """The function reads the data from a specified path and formats it into
     the required structure for further processing.
    Parameters
    ----------
    path_to_data : str
        Path to the .csv file that contains the recorded data.
    Returns
    -------
    test_df : pandas.DataFrame
        Formatted dataframe -  sensor values scaled, ordered and renamed
        columns.
    """
    '''
    _file = open(path_to_data, 'r')
    data = _file.read()
    _file.close()

    metadata = [line for line in data.split('\n') if '#' in line]
    for line in metadata:
        if line.find('Frame#') == -1:
            data = data.replace("{}".format(line), '', 1)

    acceleration_divisor = get_metadata_info_acceleration_divisor(metadata)
    gyroscope_divisor = get_metadata_info_gyroscope_divisor(metadata)
    magnetometer_divisor = get_metadata_info_magnetometer_divisor(metadata)
    pressure_divisor = get_metadata_info_pressure_divisor(metadata)
    raw2voltage_emg_divisor = get_metadata_info_emg_divisor(metadata)
    contact2impedance_divisor = get_metadata_info_contact_divisor(metadata)

    emg_order = get_metadata_info_emg_order(metadata)
    emg_columns_ordered = order_emg_columns(emg_order)

    test_df = string2dataFrame(data)

    test_df = rename_columns(test_df, emg_columns_ordered)

    test_df = scale_accelerometer_data(test_df, acceleration_divisor)
    test_df = scale_gyroscope_data(test_df, gyroscope_divisor)
    test_df = scale_magnetometer_data(test_df, magnetometer_divisor)
    test_df = scale_pressure_data(test_df, pressure_divisor)
    test_df = scale_emg_data(test_df, raw2voltage_emg_divisor)
    test_df = scale_contact_data(test_df, contact2impedance_divisor)

    return test_df
