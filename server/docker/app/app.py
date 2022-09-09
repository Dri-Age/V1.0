# Import all modules.
from flask import Flask, render_template, request
import cv2
import pytesseract
import imutils
import numpy as np

# This initializes the Flask App.
app = Flask(__name__)

# Taken from: https://github.com/zhangluustb/detect-MRZ
def read_img():
    # initialize a rectangular and square structuring kernel
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 5))
    sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21))
    # load the image, resize it, and convert it to gray scale
    image = cv2.imread("xyz.png")
    image = imutils.resize(image, height=600)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # smooth the image using a 3x3 Gaussian, then apply the black hat
    # morphological operator to find dark regions on a light background
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    black_hat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKernel)
    # compute the scharr gradient of the black hat image and scale the
    # result into the range [0, 255]
    gradX = cv2.Sobel(black_hat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    gradX = np.absolute(gradX)
    (minVal, maxVal) = (np.min(gradX), np.max(gradX))
    gradX = (255 * ((gradX - minVal) / (maxVal - minVal))).astype("uint8")
    # apply a closing operation using the rectangular kernel to close
    # gaps in between letters -- then apply Otsu's thresholding method
    gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
    thresh = cv2.threshold(gradX, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # perform another closing operation, this time using the square
    # kernel to close gaps between lines of the MRZ, then perform a
    # series of erosion to break apart connected components
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)
    thresh = cv2.erode(thresh, None, iterations=4)
    # during thresholding, it's possible that border pixels were
    # included in the thresholding, so let's set 5% of the left and
    # right borders to zero
    p = int(image.shape[1] * 0.05)
    thresh[:, 0:p] = 0
    thresh[:, image.shape[1] - p:] = 0
    # find contours in the thresholding image and sort them by their size
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    # loop over the contours
    for c in contours:
        # compute the bounding box of the contour and use the contour to
        # compute the aspect ratio and coverage ratio of the bounding box
        # width to the width of the image
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)
        crWidth = w / float(gray.shape[1])
        # check to see if the aspect ratio and coverage width are within
        # acceptable criteria -- DIDN'T WORK, SO WE OMITTED
        # COVERAGE WIDTH
        if ar > 5:
            # pad the bounding box since we applied erosion and now need
            # to re-grow it
            pX = int((x + w) * 0.03)
            pY = int((y + h) * 0.03)
            (x, y) = (x - pX, y - pY)
            (w, h) = (w + (pX * 2), h + (pY * 2))
            # extract the ROI from the image and draw a bounding box
            # surrounding the MRZ
            roi = image[y:y + h, x:x + w].copy()
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            break

    # This sets the path for the tesseract engine.
    pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
    # This reads the extracted image of the MRZ and returns the ocr string.
    text = pytesseract.image_to_string(roi, lang="ocrb")
    return text

# This is a fallback route to index.
@app.route('/')
def index():
    return 'index EMPTY'

# This is used to receive uploaded data via POST request.
# It then stores the data as image and uses the 'read_img'
# function before returning its answer
@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save("xyz.png")
        label = read_img()
        return label
    else:
        return 'error'

# This runs the app on the server.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
