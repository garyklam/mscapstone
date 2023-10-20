import os
import cv2
import numpy as np
from random import randint
from PIL import Image
from skimage import io
from skimage.util import random_noise, img_as_ubyte
from skimage.transform import rotate


destination = 'C:\\Users\\garyk\\Downloads\\Capstone\\selectset_train_aug'
holding = 'C:\\Users\\garyk\\Downloads\\Capstone\\selectset_train'
filecounts = {}
count = 1
for dir in os.listdir(holding):
    os.mkdir(os.path.join(destination, dir))
    filecounts[dir] = 0
    for filename in os.listdir(os.path.join(holding,dir)):
        if filename.endswith('.jpg') or filename.endswith('.JPG'):
            with Image.open(os.path.join(holding, dir, filename)) as img:
    #
                img.save(f'{destination}\\{dir}\\{filecounts[dir]}.jpg')
    #
                vert_img = img.transpose(Image.FLIP_TOP_BOTTOM)
                vert_img.save(f'{destination}\\{dir}\\{filecounts[dir]}_v.jpg')
    #
                horz_img = img.transpose(Image.FLIP_LEFT_RIGHT)
                horz_img.save(f'{destination}\\{dir}\\{filecounts[dir]}_h.jpg')
    #
                image = io.imread(os.path.join(holding, dir, filename))
    #
                angle = randint(10, 170)
                r_image = rotate(image, angle=angle)
                r_image = img_as_ubyte(r_image)
                r_image = cv2.cvtColor(r_image,cv2.COLOR_BGR2RGB)
                cv2.imwrite(f'{destination}\\{dir}\\{filecounts[dir]}_r1.jpg', r_image)

                angle = randint(10, 170)
                r1_image = rotate(image, angle=-angle)
                r1_image = img_as_ubyte(r1_image)
                r1_image = cv2.cvtColor(r1_image, cv2.COLOR_BGR2RGB)
                cv2.imwrite(f'{destination}\\{dir}\\{filecounts[dir]}_r2.jpg', r1_image)
    #
                new_width = int(image.shape[1] * 2)
                new_height = int(image.shape[0] * 2)
                scaled_img = cv2.resize(image, (new_width, new_height))
                x, y = randint(-40, 40), randint(-40, 40)
                scaled_img = scaled_img[112+x: 336+x,
                      112+y: 336+y,:]
                scaled_img = img_as_ubyte(scaled_img)
                scaled_img = cv2.cvtColor(scaled_img, cv2.COLOR_BGR2RGB)
                cv2.imwrite(f'{destination}\\{dir}\\{filecounts[dir]}_s.jpg', scaled_img)
    #
                x, y = randint(40, 40), randint(-40, 40)
                t_matrix = np.float32([[1, 0, x], [0, 1, y]])
                t_img = cv2.warpAffine(image, t_matrix, (image.shape[1], image.shape[0]))
                t_img = img_as_ubyte(t_img)
                t_img = cv2.cvtColor(t_img, cv2.COLOR_BGR2RGB)
                cv2.imwrite(f'{destination}\\{dir}\\{filecounts[dir]}_t1.jpg', t_img)

                x, y = randint(-60, 60), randint(-60, 60)
                t2_matrix = np.float32([[1, 0, x], [0, 1, y]])
                t1_img = cv2.warpAffine(image, t2_matrix, (image.shape[1], image.shape[0]))
                t1_img = img_as_ubyte(t1_img)
                t1_img = cv2.cvtColor(t1_img, cv2.COLOR_BGR2RGB)
                cv2.imwrite(f'{destination}\\{dir}\\{filecounts[dir]}_t2.jpg', t1_img)

                noisy = random_noise(image, mode='s&p')
                noisy = img_as_ubyte(noisy)
                noisy = cv2.cvtColor(noisy, cv2.COLOR_BGR2RGB)
                cv2.imwrite(f'{destination}\\{dir}\\{filecounts[dir]}_n.jpg', noisy)

                blurry = cv2.GaussianBlur(image, (9,9),0)
                blurry = img_as_ubyte(blurry)
                blurry = cv2.cvtColor(blurry, cv2.COLOR_BGR2RGB)
                cv2.imwrite(f'{destination}\\{dir}\\{filecounts[dir]}_b.jpg', blurry)
                filecounts[dir] += 1

    print(f'{dir} finished ({count}/{len(os.listdir(holding))})')
    count += 1
count -= 1
for dir in os.listdir(destination):
    for filename in os.listdir(os.path.join(destination, dir)):
        if randint(0, 4) == 2:
            os.remove(os.path.join(destination, dir, filename))
    print(f'({count}/{len(os.listdir(holding))})')
    count -= 1
