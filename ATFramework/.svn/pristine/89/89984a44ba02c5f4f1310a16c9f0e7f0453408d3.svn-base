
#install package
# pip install imutils
# pip install scikit-image

import cv2
import os
import imutils
import numpy as np
from skimage.metrics import structural_similarity as compare_ssim
import sys
try:
    from ..log import logger
except:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))
    print(os.path.dirname(SCRIPT_DIR))
    from _log.log import logger


# [Reminder] The file path of image support ENU language ONLY.
def generate_diff_image(img_src, img_dest, img_diff):
    target_folder = os.path.dirname(img_diff)
    if not os.path.isdir(target_folder):
        os.mkdir(target_folder)
        logger(f'Folder not exists. Create target folder={target_folder}')

    # Load the two images
    img1 = cv2.imread(img_src)
    img2 = cv2.imread(img_dest)

    img_height = img1.shape[0]

    # Grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Find the difference between the two images
    # Compute the mean structural similarity index between two images (similar).
    (similar, diff) = compare_ssim(gray1, gray2, full=True)
    # similar belongs in the interval [-1, 1] with 1 represents perfect similarity
    # Perfect similarity : both images are the same (identical) [similar: 1.0]
    logger(f'Level of similarity: {similar}')

    # diff is in range [0,1] so we need to convert it to an 8-bit array in range [0,255]
    diff = (diff*255).astype("uint8")
    # cv2.imshow("Difference", diff)

    # Apply threshold. Apply both THRESH_BINARY_INV and THRESH_OTSU
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    # cv2.imshow("Threshold", thresh)

    # Calculate contours
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    for contour in contours:
        # Calculate bounding box around contour
        if cv2.contourArea(contour) > 5:
            x, y, w, h = cv2.boundingRect(contour)
            # Draw rectangle - bounding box on both images
            cv2.rectangle(img1, (x, y), (x+w, y+h), (0,0,255), 2)
            cv2.rectangle(img2, (x, y), (x+w, y+h), (0,0,255), 2)

    # Show images with rectangles on differences
    x = np.zeros((img_height,10,3), np.uint8)
    result = np.hstack((img1, x, img2))
    cv2.imwrite(img_diff, result)
    return similar
