import Image
import ImageDraw
import ImageChops
import ImageOps
import ImageFilter

import whistler

from random import randint, choice, randrange

imgs = [ Image.open("./brushes/pointillism/brush"+str(x)+".png") for x in range(1,39)]

#colors hard coded for now, but not much effort to have them configurable like min & max values for beziers.
colors = [(255, 163, 31), (250, 155, 155), (44,16,66), (50, 53, 100), (152, 131, 91), (8,8, 127), (128, 181, 3), (162, 76, 96), (0, 79, 6), (167, 220, 250), (245, 225, 156), (187, 0, 10), (250, 250, 2), (31, 8, 60), (88, 47, 45)]

def vary(color):
    new_color = list(color)
    rc = choice([0,1,2])
    new_color[rc]  = max(0, min(255,color[rc] + randrange(-8,8)))
    #assert new_color[rc] > -1 and new_color[rc] < 256
    return tuple(new_color)
    
def varyb(color):
    new_color = list(color)
    #rc = choice([0,1,2])
    brightness = randrange(-4,4)
    new_color[0]  = max(0, min(255,color[0] + brightness))
    new_color[1]  = max(0, min(255,color[1] + brightness))
    new_color[2]  = max(0, min(255,color[2] + brightness))
    #assert new_color[rc] > -1 and new_color[rc] < 256
    return tuple(new_color)

def draw_and_compare():
    #global save_im, remaining, fail_count, last_saved_count
    global colors
    
    save_im_copy = whistler.save_im.copy()

    #poly_rect_area = get_rand_rect()

    rx1, ry1 = randint(0, whistler.width), randint(0, whistler.height)
    rim = choice(imgs)
    canvasOffset = 0
    rx1 = (rx1 - ((rx1 - canvasOffset) % rim.size[0]));
    ry1 = (ry1 - ((ry1 - canvasOffset) % rim.size[1]));
        #rim = rim.transpose(Image.FLIP_LEFT_RIGHT)

    offset = choice([1,2,3,4,5,6])
    if offset==1:
        rx1 = rx1 - rim.size[0]/2
        ry1 = ry1 - rim.size[1]/2
    if offset==2:
        rx1 = rx1 - rim.size[0]/2
        ry1 = ry1 + rim.size[1]/2
    if offset==3:
        rx1 = rx1 + rim.size[0]/2
        ry1 = ry1 - rim.size[1]/2
    if offset==4:
        rx1 = rx1 + rim.size[0]/2
        ry1 = ry1 + rim.size[1]/2
    rangle = randint(0,359)
    rim = rim.rotate(rangle, Image.NEAREST, expand=True)
    if choice([1,2]) == 2:
        rim = rim.transpose(Image.FLIP_LEFT_RIGHT)
    if choice([1,2]) == 2:
        rim = rim.transpose(Image.FLIP_TOP_BOTTOM)
    
    rx2 = rx1 + rim.size[0]
    ry2 = ry1 + rim.size[1]

    #save_im_crop = whistler.save_im.crop((rx1, ry1, rx2, ry2))
    #save_im_crop.load()
    #draw_rand_polys(save_im_crop)

    im_crop = whistler.im.crop((rx1, ry1, rx2, ry2))
    save_im_copy_crop = save_im_copy.crop((rx1, ry1, rx2, ry2))    
    im_crop.load(), save_im_copy_crop.load()

    r,g,b = varyb(vary(choice(colors)))
    
    rc, bc, bc, ralpha = rim.split()
    
    blob = ImageOps.colorize(ImageOps.grayscale(rim.convert('RGB')),(r,g,b,0), (255,255,255,0))
    #blob = rim.convert('RGB')
    blob.filter(ImageFilter.BLUR)
    ralpha.filter(ImageFilter.BLUR)
    blob.putalpha(ralpha)
    whistler.save_im.paste(blob,
                 (rx1, ry1), mask=ralpha)
    painted_crop = whistler.save_im.crop((rx1, ry1, rx2, ry2))
    painted_crop.load()

    old_diff = whistler.abs_diff(save_im_copy_crop,im_crop)
    new_diff = whistler.abs_diff(painted_crop,im_crop)
    
    if new_diff < old_diff:
        whistler.remaining -= old_diff-new_diff
        #print ':\timproved\t' + str(old_diff-new_diff)\
        #             + '\tremaining:\t' + str(remaining)
        whistler.last_saved_count = 0
        whistler.fail_count=0
    else:
        whistler.save_im = save_im_copy
        whistler.fail_count +=1
