import cv2
import numpy as np


class Frame:
    def __init__(self, x_top_left: int, y_top_left: int,
                 x_bottom_right: int, y_bottom_right:int,
                 x1: float, y1: float,
                 x0: float = 0, y0: float = 0):
        self.x_top_left = x_top_left
        self.y_top_left = y_top_left
        self.x_bottom_right = x_bottom_right
        self.y_bottom_right = y_bottom_right
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1

    def crop_gray(self, img: np.ndarray) -> np.ndarray:
        return img[self.y_top_left:self.y_bottom_right, self.x_top_left:self.x_bottom_right]

    def compare_y(self, y):
        delta_frame = self.y_bottom_right - self.y_top_left
        delta_plot = self.y1-self.y0
        return self.y1-delta_plot/delta_frame * y

    def compare_x(self, x):
        delta_frame = self.x_bottom_right - self.x_top_left
        delta_plot = self.x1 - self.x0
        return delta_plot / delta_frame * x


class Converter:
    def imgplot2vec(self, img, frame:Frame):
        img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        area = frame.crop_gray(img_gray)
        w = area.shape[1]
        y_vec = np.zeros(w)
        x_vec = np.zeros(w)
        for i in range(w):
            yi = np.argmin(area[:, i])
            y_vec[i] = frame.compare_y(yi)
            x_vec[i] = frame.compare_x(i)
        return y_vec, x_vec
