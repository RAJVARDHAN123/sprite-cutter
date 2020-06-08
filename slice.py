# ===========================================
# Spritesheet cutter/slicer by Sunny
# https://github.com/sunnypwang/sprite-cutter
# ===========================================

import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filename', help='sprite sheet filename')
parser.add_argument('--w', required=False, default=16, help='output width')
parser.add_argument('--h', required=False, default=16, help='output height')
args = parser.parse_args()

filename = args.filename
WIDTH = int(args.w)
HEIGHT = int(args.h)
path = filename.split('.')[0]

sheet = plt.imread('{}'.format(filename))

# Add alpha channel
if(sheet.shape[-1] < 4):
    sheet = np.append(sheet, np.ones(
        (sheet.shape[0], sheet.shape[1], 1)), axis=-1)
print(sheet.shape)

# Output dir
if not os.path.exists(path):
    os.mkdir(path)

# Background color
bg = np.array([1., 1., 1., 0.])
if not np.array_equal(sheet[0, 0], bg):
    bg = sheet[0, 0]
print('blank:', bg)

# Cut into row chunks by finding an image row with all bg pixel
last_i = -1
rows = []
n = 0
for i, r in enumerate(sheet):
    # print(i, r.mean(axis=0))
    if np.array_equal(r.mean(axis=0), bg):
        # if r.mean(axis=0)[-1] == 0:
        last_i += 1
        if i != last_i:
            print(last_i, i)
            sub = sheet[last_i:i]
            rows.append(sub)
            n += 1
            last_i = i
print(len(rows))


# Cut into sprites for each row by finding an image column with all bg pixel
N = 0
for i, sub in enumerate(rows):
    sub[sub >= 0.99] = 1.
    last_j = -1
    max_w = 0
    max_h = 0
    # print(i)
    n = 0
    for j, c in enumerate(sub.mean(axis=0)):

        if np.array_equal(c, bg):
            # if c[-1] == 0.0:

            if j != last_j+1:
                tmp = sub[:, last_j:j]
                w, h = tmp.shape[1], tmp.shape[0]
                pad_w_l = max(0, (WIDTH-w)//2)
                pad_w_r = max(0, (WIDTH-w+1)//2)
                pad_h = max(0, (HEIGHT-h))
                tmp2 = np.pad(tmp, ((pad_h, 0), (pad_w_l, pad_w_r), (0, 0)), mode='constant', constant_values=(
                    (bg, bg), (bg, bg), (0, 0)))
                # print(i, n, tmp2.shape, tmp.shape)
                n += 1
                N += 1
                plt.imsave(path + '/{}_{}.png'.format(i, n), tmp2)

            last_j = j
print('Total {} sprites'.format(N))
