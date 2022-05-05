# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 17:47:00 2022

@author: kipri
"""

import cv2
import time
import sys
import os
from ffpyplayer.player import MediaPlayer


def play_video(video_name, file_name):

    cap = cv2.VideoCapture(video_name)
    player = MediaPlayer(video_name)
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    cv2.namedWindow("video", cv2.WND_PROP_FULLSCREEN)
    cv2.moveWindow("video", 1920, 0)
    cv2.setWindowProperty(
        "video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    start = time.time()
    while(cap.isOpened()):
        ret, frame = cap.read()
        audio_frame, val = player.get_frame()
        if not ret:
            #print("Reached end of video, exiting.")
            end = time.time()
            break

        #frame = cv2.resize(frame, (1500, 800))
        cv2.imshow("video", frame)

        elapsed = (time.time() - start) * 1000  # msec
        play_time = int(cap.get(cv2.CAP_PROP_POS_MSEC))
        sleep = max(1, int(play_time - elapsed))

        if cv2.waitKey(int(sleep)) & 0xFF == ord('q'):
            break

        if val != 'eof' and audio_frame is not None:
            img, t = audio_frame

       
    f = open(file_name, "a")
    f.write(video_name + '\n')
    f.write('Start: ' + str(start) + '; End: ' + str(end) + '\n')
    f.close()

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    path_to_data = r"C:\Users\kipri\OneDrive\Desktop\OpenFace Data Collection"
    video_name = sys.argv[1]
    file_name = sys.argv[2]
    print(video_name)
    play_video(path_to_data+os.sep+video_name, file_name)
