# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 15:45:59 2022

@author: simon
"""

import cv2
import numpy as np
import pandas as pd
import os
import json
import tensorflow as tf
from tensorflow.keras.models import Model, Sequential, \
     load_model, model_from_json

from facial_analysis import FacialImageProcessing


def load_video(path_to_video):
    '''
    

    Parameters
    ----------
    path_to_video : TYPE
        DESCRIPTION.

    Returns
    -------
    video : TYPE
        DESCRIPTION.

    '''
    video = cv2.VideoCapture(path_to_video)
    return video


def get_frameCount(video):
    '''
    

    Parameters
    ----------
    video : TYPE
        DESCRIPTION.

    Returns
    -------
    frame_count : TYPE
        DESCRIPTION.

    '''
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    return frame_count


def get_fps(video):
    '''
    

    Parameters
    ----------
    video : TYPE
        DESCRIPTION.

    Returns
    -------
    fps : TYPE
        DESCRIPTION.

    '''
    fps = video.get(cv2.CAP_PROP_FPS)
    return fps


def mobilenet_preprocess_input(x):
    '''
    

    Parameters
    ----------
    x : TYPE
        DESCRIPTION.
    **kwargs : TYPE
        DESCRIPTION.

    Returns
    -------
    x : TYPE
        DESCRIPTION.

    '''
    inp = x.astype(np.float32)
    inp[..., 0] -= 103.939
    inp[..., 1] -= 116.779
    inp[..., 2] -= 123.68
    inp = np.expand_dims(inp, axis=0)
    return inp


def display_detected_emotions(frame, detected_emotion):
    '''
    

    Parameters
    ----------
    frame : TYPE
        DESCRIPTION.
    detected_emotion : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    # Describe the type of font to be used.
    font = cv2.FONT_HERSHEY_SIMPLEX
    # Use putText() method for inserting text on video
    cv2.putText(frame, detected_emotion, (50, 50),
                font, 1, (0, 255, 255),
                2, cv2.LINE_4)
    # Display the resulting frame
    cv2.imshow("In progress", frame)


def process_video(video, number_of_frames, imgProcessing, model,
                  show_detection):
    '''
    

    Parameters
    ----------
    video : TYPE
        DESCRIPTION.
    number_of_frames : TYPE
        DESCRIPTION.
    imgProcessing : TYPE
        DESCRIPTION.
    model : TYPE
        DESCRIPTION.

    Returns
    -------
    predictions : TYPE
        DESCRIPTION.

    '''
    frame_count = 0
    predictions = []  # Store detected emotions

    while frame_count < number_of_frames:
        _, frame = video.read()

        # Use later for displaying the detected emotions
        raw_frame = frame.copy()

        # Detect faces in the frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        bounding_boxes, points = imgProcessing.detect_faces(frame)
        points = points.T

        
        # Iterate through the detected faces and detect their emotion
        for bbox, p in zip(bounding_boxes, points):
            # Change the bounding boxes to int
            box = bbox.astype(np.int)
            # Select the x,y coordinates
            x1, y1, x2, y2 = box[0:4]
            # Cut the frame using the detected bouding box cooridinates
            face_img = frame[y1:y2, x1:x2, :]
            face_img = cv2.resize(face_img, INPUT_SIZE)
            # Adjust the frame for the appropriate architecture
            inp = mobilenet_preprocess_input(face_img)
            # Predict the emotion of the detected face
            scores = model.predict(inp)[0]

            # Save the prediction for the current frame
            predictions.append(scores)
        
        # If we want to show the detections
        if show_detection:
            if "scores" in locals():
                display_detected_emotions(raw_frame,
                                          idx_to_class[np.argmax(scores)])
            else:
                display_detected_emotions(raw_frame, "None")
            # creating 'q' as the quit button for the video
            if cv2.waitKey(1) & 0xFF == ord('q'):
                # release the cap object
                video.release()
                # close all windows
                cv2.destroyAllWindows()
                break

    return predictions


def process_predictions(predictions):
    '''
    

    Parameters
    ----------
    predictions : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    # Get all prediction probabilities, with column names
    predict_proba = pd.DataFrame(predictions)
    predict_proba.columns = idx_to_class.values()

    # Get finally prediction per frame
    predictions = np.argmax(predictions.values, axis=1)

    return predict_proba, predictions


if __name__ == "__main__":

    # Path to data where the videos are stored
    path_to_video = ".." + os.sep + "videos" + os.sep + "Matej.avi"

    # Path to the pretrained model
    path_to_models = ".." + os.sep + "models" + os.sep + "affectnet_emotions"
    model = "mobilenet_7.h5"

    # Path where the detections will be stored
    path_to_result = ".." + os.sep + "annotations"

    # Define constants
    INPUT_SIZE = (224, 224)
    idx_to_class = {0: 'Anger', 1: 'Disgust', 2: 'Fear', 3: 'Happiness',
                    4: 'Neutral', 5: 'Sadness', 6: 'Surprise'}

    # 0 - Don't show the video, 1- Show video with detections
    show_detection = 1

    # Load model
    model = load_model(path_to_models + os.sep + model)
    print(model.summary())

    # Load video for analysis
    video = load_video(path_to_video)

    # Get video metadata
    number_of_frames = get_frameCount(video)
    fps = get_fps(video)
    duration = number_of_frames/fps

    # Initilize an object for various image manipulations
    imgProcessing = FacialImageProcessing()

    # Process the video and get predictions
    predictions = process_video(video, number_of_frames, imgProcessing, model,
                                show_detection)

    # Generate dataframes with prediction probabilities and finally prediction
    predict_proba, predict = process_predictions(predictions)
    predict_proba.to_csv(path_to_result + os.sep + "probabilities.csv",
                         index=False)
    predict.to_csv(path_to_result + os.sep + "predictions.csv",
                   index=False)
