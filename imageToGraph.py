import cv2
import matplotlib.pyplot as plt
import numpy as np



def scale_down(img, scale_percent):
    img = cv2.resize(img, (int(img.shape[1] * scale_percent / 100), int(img.shape[0] * scale_percent / 100)),
                     interpolation=cv2.INTER_AREA)
    return img


def define_borders(img, color_of_border):
    mask = cv2.inRange(img, np.array([color_of_border - 5]), np.array([color_of_border + 5]))
    img[mask > 0] = 0
    return img


def dilate_edge(img, amount):
    kernel = np.ones((amount, amount), np.uint8)
    img = cv2.erode(img, kernel, iterations=1)
    return img


def ready_image():
    img = cv2.imread(r"C:\Users\shree\OneDrive\Pictures\obstacles.png",
                     cv2.IMREAD_GRAYSCALE)  # stores grayscale image in img
    # post processing to make edges well defined.
    img = define_borders(img, 205)
    #img = scale_down(img, 5)
    #img = dilate_edge(img, 1)
    #plt.imshow(img, cmap='gray')
    return img

def get_obstacle(x,y):
    try:
        if img[round(y)][round(x)] == 0:
            return True
        else:
            return False
    except:
        return True

def get_all_points(img):
    a = np.where(img == [255])
    coord = zip(a[1], a[0])
    l = list(coord)
    return list(l)
#plt.figure("post_processing")
#plt.imshow(img, cmap='gray')

img = ready_image()
