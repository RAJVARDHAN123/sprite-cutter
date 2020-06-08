import sys
import os
import glob
from PIL import Image
import argparse

parser = argparse.ArgumentParser(
    description='Support 3 actions - GIF to Sheet, GIF to Images, Sheet to GIF')
parser.add_argument(
    'filename', help='Image file. Supports GIF mode and Image mode')
parser.add_argument('--sheet', metavar='AS_SHEET', type=bool, default=False,
                    help='Boolean. Use in GIF mode. Tells whether output is a single sheet image (True) or multiple images (False)')
parser.add_argument('--n', metavar='SUBIMG', type=int, default=0,
                    help='Integer. Use in Image mode. Specifies the number of subimages in a sheet image')
args = parser.parse_args()

filename = args.filename
sheet = args.sheet
n = args.n


def gif2img(filename, sheet=False):
    name = filename.split('.')[0]
    with Image.open(filename) as im:
        n = im.n_frames
        print('Number of frames: ', n)

        if sheet:
            new_im = Image.new('RGBA', (im.width * n, im.height))
            for i in range(n):
                im.seek(i)
                new_im.paste(im, (im.width*i, 0))
            new_im.save('{}_sheet.png'.format(name))
        else:
            if not os.path.exists(name):
                os.mkdir(name)
            for i in range(n):
                im.seek(i)
                im.save(os.path.join(name, '{}.png'.format(i)))


def sheet2gif(filename, n):
    name = filename.split('.')[0]
    with Image.open(filename) as im_sheet:
        w = im_sheet.width // n
        h = im_sheet.height
        # im_gif = Image.new('RGBA', (w, h))
        x, y = 0, 0
        subs = []
        for i in range(n):
            subs.append(im_sheet.crop((x+i*w, y, x+(i+1)*w, y+h)))
        im_gif = subs[0]
        im_gif.save('{}.gif'.format(name), format='GIF',
                    append_images=subs[1:], save_all=True, duration=100, loop=0, disposal=2, transparency=0)
        # print(im_sheet.transparency)


if filename.endswith('.gif'):
    if sheet:
        print('Converting GIF to Sheet')
    else:
        print('Converting GIF to Images')
    gif2img(filename, sheet)
else:
    print('Converting Sheet to GIF')
    sheet2gif(filename, n)
