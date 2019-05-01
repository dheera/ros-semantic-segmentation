#!/usr/bin/env python3

import cv2
from cv_resize import resize

img = cv2.imread("/home/dheera/foo2.jpg")
img2 = resize(img, (400, 400))
cv2.imshow('foo', img2)
cv2.waitKey(0)

