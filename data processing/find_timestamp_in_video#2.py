
import cv2


def load_video(path_to_video):
    video = cv2.VideoCapture(path_to_video)
    return video


def get_frameCount(video):
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    return frame_count


def get_fps(video):
    fps = video.get(cv2.CAP_PROP_FPS)
    return fps


def show_image(video, fps, second, frame):
    video.set(cv2.CAP_PROP_POS_FRAMES, second * fps + frame)
    success, image = video.read()
    # Show the image
    cv2.imshow("Frame Name", image)
    # To load and hold the image
    cv2.waitKey(0)
    # To close the window after the required kill value was provided
    cv2.destroyAllWindows()


def calculate_timestamp(path_to_video, fps, second, frame):
    # Get the starting timestamp of the video from the name of the video file
    video_start_timestamp = float(path_to_video.split('\\')[-1].split('-')[0])

    timestamp = video_start_timestamp + (second + frame * (1 / fps))
    return timestamp


if __name__ == "__main__":
    frame = 0
    for framee in range (0,20,1):
        path_to_video = r"C:\Users\Andrej\Desktop\DATASCIENCE\Praksa\Participant\Participant 13\TaskA\1651836179.1571956 - output.avi"
        video = load_video(path_to_video)
        frame_count = get_frameCount(video)
        fps = get_fps(video)

        second = 35 #value of seconds
        frame = frame + 1 # value from 0 to FPS
        show_image(video, fps, second, frame)
        print(frame)
        timestamp = calculate_timestamp(path_to_video, fps, second, frame)
        print(timestamp)
