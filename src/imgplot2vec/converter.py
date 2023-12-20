import cv2
import numpy as np


class Frame:
    def __init__(self, x_top_left: int, y_top_left: int,
                 x_bottom_right: int, y_bottom_right: int,
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
    def imgplot2vec(self, img, frame: Frame):
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


class AutoConverter(Converter):
    def auto_imgplot2vec(self, img,  max_frame=0.05, max_intensity=80):
        img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        bottom_bord = self._auto_frame(img_gray, type_border="bottom", max_frame=max_frame, max_intensity=max_intensity)
        top_bord = self._auto_frame(img_gray, type_border="top", max_frame=max_frame, max_intensity=max_intensity)
        left_bord = self._auto_frame(img_gray, type_border="left", max_frame=max_frame, max_intensity=max_intensity)
        right_bord = self._auto_frame(img_gray, type_border="right", max_frame=max_frame, max_intensity=max_intensity)
        frame = Frame(left_bord, top_bord, right_bord, bottom_bord, 1, 1)
        return self.imgplot2vec(img, frame)

    def _auto_frame(self, img_gray, type_border="bottom", max_frame=0.05, max_intensity=80):
        invimg = (255 - img_gray[:, :])
        if type_border in ("bottom", "top"):
            dim = invimg[1:, :].mean(1) - invimg[:-1, :].mean(1)
        elif type_border in ("left", "right"):
            dim = invimg[:, 1:].mean(0) - invimg[:, :-1].mean(0)
        else:
            raise ValueError('type_border in (bottom, top, left, right)')

        len_dim = len(dim)
        delta_frame = round(len_dim * max_frame)
        abs_dim = abs(dim)
        if type_border in ("bottom", "right"):
            return len_dim - delta_frame + self.__first_max_intensity(abs_dim[len_dim - delta_frame:], max_intensity)
        else:
            return self.__end_max_intensity(abs_dim[:delta_frame], max_intensity)

    def __first_max_intensity(self, dim, max_intensity):
        i = 0
        for val in dim:
            if val > max_intensity:
                return i
            else:
                i += 1
        return i

    def __end_max_intensity(self, dim, max_intensity):
        i = len(dim)
        for val in reversed(dim):
            if val > max_intensity:
                return i
            else:
                i -= 1
        return i
