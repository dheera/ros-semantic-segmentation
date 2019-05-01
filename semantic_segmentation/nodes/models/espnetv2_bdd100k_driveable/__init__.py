#!/usr/bin/env python3

import json
import os
import numpy as np
import time
import torch
from .cnn import SegmentationModel as net
from .cv_resize import resize

PATH = os.path.dirname(__file__)
SCALE = 1.0
WEIGHTS_FILENAME = "weights.pth"
CATEGORIES_FILENAME = "categories.json"
INPUT_WIDTH = 1024
INPUT_HEIGHT = 512
USE_GPU = True
MEAN = np.array([[[72.3923111, 82.90893555, 73.15840149]]], dtype = np.float32)
STD = np.array([[[45.3192215, 46.15289307, 44.91483307]]], dtype = np.float32)

class Model(object):
    def __init__(self):
        color_map_list = []
        with open(os.path.join(PATH, CATEGORIES_FILENAME)) as f:
            self._categories = json.loads(f.read())
            self._color_map = np.array([category["color"] for category in self._categories], dtype = np.uint8)

        self.model = net.EESPNet_Seg(len(self._categories), s = SCALE)

        self.model = torch.nn.DataParallel(self.model)
        self.model.load_state_dict(torch.load(os.path.join(PATH, WEIGHTS_FILENAME)))
        if USE_GPU:
            self.model = self.model.cuda()

        self.model.eval()

    @property
    def trace(self):
        return (self.run_options.trace_level > 0)

    @trace.setter
    def trace(self, value):
        if value:
            self.run_options.trace_level = tf.RunOptions.FULL_TRACE
        else:
            self.run_options.trace_level = 0

    @property
    def color_map(self):
        return self._color_map

    @property
    def categories(self):
        return self._categories

    def infer(self, images):
        # TODO: support batch size > 1

        img = images[0]
        img = img.astype(np.float32)
        img = resize(img, (INPUT_WIDTH, INPUT_HEIGHT))
        img -= MEAN
        img /= STD

        img = img / 255
        img = img.transpose((2, 0, 1))

        img_tensor = torch.from_numpy(img)
        img_tensor = torch.unsqueeze(img_tensor, 0)

        if USE_GPU:
            img_tensor = img_tensor.cuda()

        img_out = self.model(img_tensor)
        classMap_numpy = img_out[0].max(0)[1].byte().cpu().data.numpy()
        return [classMap_numpy]

