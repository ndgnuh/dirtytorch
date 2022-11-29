import cv2
from typing import Callable


class FrameThrottle:
    """
    Handle only the clearest frames in a video or a video stream
    """

    def __init__(self, callback: Callable, fps=24):
        self.fps = fps
        self.callback = callback
        self.selected_frame = None
        self.max_clear = -1
        self.nframes = 0

    def __call__(self, frame):
        if self.nframes < self.fps:
            self.nframes += 1
            clear = cv2.Laplacian(frame, cv2.CV_8UC3).var()
            if clear > self.max_clear:
                self.max_clear = clear
                self.selected_frame = frame
        else:
            self.callback(self.selected_frame)
            self.nframes = 0
            self.selected_frame = None
            self.max_clear = -1
