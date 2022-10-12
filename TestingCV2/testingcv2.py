import cv2
import time
import numpy as np
from statistics import mean
import copy

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


# Read the pixels from a binary image utilising Rolling Shutter Principles
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
    if ((T_tx % T_row != 0) and (T_tx != T_row)) or T_tx < T_row:
        raise Exception("Incompatible Ftx and Fs")
    else:
        # Increment for loop by (T_tx//T_row) pixels because of transmission freq
        for i in range(ybuff, img_h - ybuff, int(T_tx // T_row)):
            if img[i, img_c] == 255:
                output.append(1)
            else:
                output.append(0)
    return output


# Incomplete function for reading data. Need to finalise encoding first.
def readData(out_arr):
    preamble = np.array([1, 1, 1, 1, 1, 1, 0])
    np_arr = np.array(out_arr)
    # for i in range(len(np_arr)):


def getRowsOutput(roi, thresh):
    outArr = []
    for ind, row in enumerate(roi):
        if mean(row) >= thresh:
            roi[ind] = np.multiply(np.ones(len(row)), 255)
            outArr.append(1)
        else:
            roi[ind] = np.zeros(len(row))
            outArr.append(0)
    return outArr


def processRowsOutput(rowArr):
    outArr = []
    counter = 0
    for i in range(1, len(rowArr)):
        if rowArr[i-1] == rowArr[i]:
            counter += 1
        else:
            outArr.append((counter, rowArr[i-1]))
            counter=0
    outArr.append((counter, rowArr[i]))
    return outArr


def ReadLight():
    # All of these can be set using a detection library
    roi_x = 490
    roi_y = 360
    roi_w = 350
    roi_h = 350

    # cap = cv2.VideoCapture(1)  # Select web cam 0
    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    cap = cv2.VideoCapture()
    cap.open(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FOURCC, fourcc)

    cam_w_4k = 3840
    cam_h_4k = 2160
    cam_w_1080 = 1920
    cam_h_1080 = 1080
    frame_rate_1080 = 30
    frame_rate_4k = 30
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, cam_w_1080)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_w_1080)
    cap.set(cv2.CAP_PROP_FPS, frame_rate_1080)
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1) # Set to 3 for auto and 1 for manual
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    cap.set(cv2.CAP_PROP_EXPOSURE, -11) # Minimum Allowable Exposure
    cap.set(cv2.CAP_PROP_FOCUS, 255)
    # print('Exposure: ', cap.get(cv2.CAP_PROP_EXPOSURE))
    print("FR: ", cap.get(cv2.CAP_PROP_FPS))
    print("Focus", cap.get(cv2.CAP_PROP_FOCUS))
    # change on change of cam dims
    cam_h = cam_h_1080
    cam_w = cam_w_1080

    # cap.set(3, cam_w)
    # cap.set(4, cam_h)
    previous_time = 0

    light_reader = LightReader(roi_x, roi_y, roi_w, roi_h)
    hz = round(cap.get(cv2.CAP_PROP_FPS))
    init_time = time.time()
    current_time = time.time()
    out_str = ""
    proc_out_str = ""

    linesOnScreen = 19
    lineStartCords = []
    lineEndCords = []
    for h in range(1, linesOnScreen):
        lineStartCords.append((1, h*(roi_h // linesOnScreen)))
        lineEndCords.append((249, h*(roi_h // linesOnScreen)))

    while current_time-init_time < 10:
        # Time the loop
        current_time = time.time()
        p_hz = 1 / (current_time - previous_time)
        # if p_hz > frame_rate_1080 + 1:
        #     continue
        previous_time = current_time

        # Read image and process
        success, img_r = cap.read()
        img = cv2.cvtColor(img_r, cv2.COLOR_BGR2GRAY)
        roi = getROIImage(img, roi_x, roi_y, roi_w, roi_h)

        roi = cv2.equalizeHist(roi)
        # roi_i_eq = copy.deepcopy(roi_i)
        # print(np.amax(roi_i))
        img = light_reader.draw_region(img)

        # Read the data
        outArr = getRowsOutput(roi, 80)
        out_str += str(outArr) + "\n"

        proc_out_str += str(processRowsOutput(outArr)) + "\n"
        cv2.putText(img, "Cam HZ Setting: " + str(int(hz)), (15, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
        cv2.putText(img, "Loop HZ: " + str(p_hz), (15, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
        # for j in range(linesOnScreen-1):
        #     cv2.line(roi_bin, lineStartCords[j], lineEndCords[j], (255, 0, 0), 2)
        cv2.imshow("roi", roi)
        # cv2.imshow("roi_eq", roi_i_eq)
        cv2.imshow("image", img)
        cv2.waitKey(1)

    with open('out_at_350us_T.txt', 'w') as f:
        f.write(out_str)

    with open('Proc_out_at_350us_T.txt', 'w') as f:
        f.write(proc_out_str)


if __name__ == '__main__':
    ReadLight()
