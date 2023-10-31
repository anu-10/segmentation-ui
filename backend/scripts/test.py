from model import segmentation_model
import cv2
import os
from PIL import Image
import numpy as np
segment = segmentation_model()
images = segment.segmentation()
for i in range(0, len(images), 10):
    save_path = '../segmented/saved_image'+ str(i)+'.png'
    I = images[i, :, :, 0]
    I8 = (((I - I.min()) / (I.max() - I.min())) * 255.9).astype(np.uint8)
    image = Image.fromarray(I8)
    image.save(save_path)