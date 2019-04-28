#!/usr/bin/env python3

"""
Nearest neighbor resize using numpy only.
Unfortunately the ROS-provided cv2.so is fantastically compiled without python3 bindings so it cannot be used with python3. This allows people who only need nearest neighbor resize to avoid these shenanigans entirely and avoid OpenCV dependency.

Author: dheera@dheera.net
"""

import numpy as np

def resize(img, new_shape):
    """
    Nearest-neighbor resize.
    img = an opencv image
    shape = (width, height) as per OpenCV convention NOT numpy convention
    """

    new_width, new_height = new_shape  # cv2 convention
    old_height, old_width = img.shape[0], img.shape[1]  # numpy shenanigans

    new_i, new_j = np.meshgrid(
        np.linspace(0, old_width - 1, new_width).astype(np.uint16),
        np.linspace(0, old_height -1, new_height).astype(np.uint16)
    )

    return img[new_j, new_i]
