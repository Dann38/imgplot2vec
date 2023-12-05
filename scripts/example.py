import cv2
from imgplot2vec import Reader, Frame, Converter
import matplotlib.pyplot as plt


reader = Reader()
converter = Converter()
frame = Frame(x_top_left=150, y_top_left=132, x_bottom_right=1552, y_bottom_right=912,
              x0=0, y0=0, x1=4, y1=100)


img = reader.read(r"img/1.png")
vec_y, vec_x = converter.imgplot2vec(img, frame)

gray_frame = frame.crop_gray(cv2.cvtColor(img, cv2.COLOR_RGB2GRAY))
print(vec_y, vec_x)
plt.plot(vec_x, vec_y, ".")
plt.grid()
plt.xlim([frame.x0, frame.x1])
plt.ylim([frame.y0, frame.y1])
plt.show()

# cv2.imshow(" ", gray_frame)
# cv2.waitKey()
