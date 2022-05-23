import cv2
import time
import numpy as np


class LightReader:
    def __init__(self, roi_x, roi_y, roi_w, roi_h):
        self.roi_x = roi_x
        self.roi_y = roi_y
        self.roi_w = roi_w
        self.roi_h = roi_h
        self.pt1 = [self.roi_x, self.roi_y]
        self.pt2 = [self.roi_x + self.roi_w, self.roi_y + self.roi_h]

    def draw_region(self, img):
        cv2.rectangle(img, self.pt1, self.pt2, color=(255, 0, 0), thickness=3)
        return img


def getROIImage(img, roi_x, roi_y, roi_w, roi_h):
    crop_img = img[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w]
    return crop_img


def readBinPixels(img, img_t_h, ybuff, img_Hz, tx_Hz, p_len):
    T_tx = 1 / tx_Hz
    T_t = 1 / img_Hz
    T_row = T_t / img_t_h
    img_h = img.shape[0]
    if img_h - 2 * ybuff * (T_tx / T_row) < p_len:
        raise Exception("Insufficient pixel-height")
    img_w = img.shape[1]
    img_c = img_w // 2
    output = []
    if T_tx % T_row != 0 or T_tx < T_row:
        raise Exception("Incompatible Ftx and Fs")
    else:
        # Increment for loop by (T_tx//T_row) pixels because of transmission freq
        for i in range(ybuff, img_h - ybuff, int(T_tx // T_row)):
            if img[i, img_c] == 255:
                output.append(1)
            else:
                output.append(0)
    return output

def readData(out_arr):
    preamble = np.array([1, 1, 1, 1, 1, 1, 0])
    np_arr = np.array(out_arr)
    #for i in range(len(np_arr)):




def ReadLight():
    # All of these can be set using a detection library
    roi_x = 100
    roi_y = 100
    roi_w = 150
    roi_h = 150

    cap = cv2.VideoCapture(0)  # Select web cam 0
    cam_h, cam_w = 720, 1280
    cap.set(3, cam_w)
    cap.set(4, cam_h)
    previous_time = 0

    light_reader = LightReader(roi_x, roi_y, roi_w, roi_h)
    hz = cap.get(cv2.CAP_PROP_FPS)

    while True:
        # Time the loop
        current_time = time.time()
        p_hz = 1 / (current_time - previous_time)
        if p_hz > 30:
            continue
        previous_time = current_time


        # Read image and process
        success, img_r = cap.read()
        img_g = cv2.cvtColor(img_r, cv2.COLOR_BGR2GRAY)
        # roi_i = getROIImage(img_g, roi_x, roi_y, roi_w, roi_h)
        img = light_reader.draw_region(img_g)
        # th, roi_bin = cv2.threshold(roi_i, 128, 255, cv2.THRESH_OTSU)

        # Packet length Preamble+Payload+Parity = 7+32+1 = 40
        p_len = 40
        # The sample rate of rows in camera
        tx_Hz = hz * cam_h

        # Read the data
        ybuff = 3
        out_arr = readBinPixels(img_g, cam_h, ybuff, hz, tx_Hz, p_len)
        print(out_arr)



        # Display the image(s)
        cv2.putText(img, "Cam HZ: " + str(int(hz)), (15, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
        cv2.putText(img, "Loop HZ: " + str(p_hz), (15, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
        cv2.imshow("roi", roi_bin)
        cv2.imshow("image", img)
        cv2.waitKey(1)


if __name__ == '__main__':
    ReadLight()
