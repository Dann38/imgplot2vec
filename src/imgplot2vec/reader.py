import cv2
import numpy as np


class Reader:
    def read(self, name_image_file: str) -> np.ndarray:
        path_image = name_image_file
        with open(path_image, "rb") as f:
            chunk = f.read()
        chunk_arr = np.frombuffer(chunk, dtype=np.uint8)
        image = cv2.imdecode(chunk_arr, cv2.IMREAD_COLOR)
        return image
