import Image
import ImageDraw
import ImageChops

from random import randint
import os

import argparse

import numpy

from threading import Thread

def make_bezier(xys):
    # xys should be a sequence of 2-tuples (Bezier control points)
    n=len(xys)
    combinations=pascal_row(n-1)
    def bezier(ts):
        # This uses the generalized formula for bezier curves
        # http://en.wikipedia.org/wiki/B%C3%A9zier_curve#Generalization
        result=[]
        for t in ts:
            tpowers=(t**i for i in range(n))
            upowers=reversed([(1-t)**i for i in range(n)])
            coefs=[c*a*b for c,a,b in zip(combinations,tpowers,upowers)]
            result.append(
                tuple(sum([coef*p for coef,p in zip(coefs,ps)]) for ps in zip(*xys)))
        return result
    return bezier

def pascal_row(n):
    # This returns the nth row of Pascal's Triangle
    result=[1]
    x,numerator=1,n
    for denominator in range(1,n//2+1):
        # print(numerator,denominator,x)
        x*=numerator
        x/=denominator
        result.append(x)
        numerator-=1
    if n&1==0:
        # n is even
        result.extend(reversed(result[:-1]))
    else:
        result.extend(reversed(result)) 
    return result

def get_rand_rect():
    global width, height, max_width, max_height, min_width, min_height  

    rx1, ry1 = randint(0, width-1), randint(0, height-1)
    rx2 = rx1 + randint(min_width, max_width)
    ry2 = ry1 + randint(min_height, max_height)
    
    #clip and move back if out of image bounds
    if rx2 > width-1:
        rx1 = max(0, rx1 - (rx2 -rx1))
        rx2 = width-1
    if ry2 > height-1:
        ry1 = max(0, ry1 - (ry2 -ry1))
        ry2 = height-1
    return rx1, ry1, rx2, ry2


def draw_rand_polys(im):
    global width, height
    r,g,b = randint(0,255), randint(0,255), randint(0,255)
    rcolor = 'rgb('+str(r)+','+str(g)+','+ str(b)+')'

    draw = ImageDraw.Draw(im)
    ts=[t/100.0 for t in range(101)]

    points = []
    xys = []

    rx1, ry1, rx2, ry2 = 0, 0, im.size[0]-1, im.size[1]-1
    
    for i in range(0,randint(2,6)):
        x1, y1 = randint(rx1,rx2), randint(ry1,ry2)
        x2, y2 = randint(rx1,rx2), randint(ry1,ry2)
        x3, y3 = randint(rx1,rx2), randint(ry1,ry2)
        
        xys.append([(x1,y1),(x2,y2),(x3,y3)])
    
    for idx, xy in enumerate(xys[0:-1]):
        bezier=make_bezier(xy+[xys[idx+1][0]])
        points.extend(bezier(ts))
        
    bezier=make_bezier(xys[-1]+[xys[0][0]])
    points.extend(bezier(ts))

    draw.polygon(points,fill=rcolor)
    poly_rect_area = (rx1, ry1, rx2, ry2)
    return poly_rect_area

def abs_diff(a,b):
    diff = ImageChops.difference(a,b)
    numpy.asarray(diff)
    return numpy.sum(diff)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(version='1.0',
             description="""Incremental painting program.
                           Default for all brush size arguments is a
                           number which divides into image width/height.
                           The --use-pixels flags can override this.""")
            
    parser.add_argument('image',
        help='Image file to paint e.g. pic.jpg')

    parser.add_argument('-g','--goal',type=int, default=0,
        help='Value to stop at. Absolute difference of rgb values')

    # set min and max brush sizes.            
    parser.add_argument('--xmax',type=int, default=2,
            help='Max brush size x.')
    parser.add_argument('--ymax',type=int, default=2,
            help='Max brush size y.')
    parser.add_argument('--xmin',type=int, default=16,
            help='Min brush size x.')
    parser.add_argument('--ymin',type=int, default=16,
            help='Min brush size y.')

    # these flags override default of dividing by image size with pixels
    parser.add_argument('-p','--usepixels', action='store_true',
            help='Use values in pixels for all brush sizes')
    parser.add_argument('--usepixels-xmin', action='store_true',
            help='Use a value in pixels for min brush x')
    parser.add_argument('--usepixels-xmax', action='store_true',
            help='Use a value in pixels for max brush x')
    parser.add_argument('--usepixels-ymin', action='store_true',
            help='Use a value in pixels for min brush y')
    parser.add_argument('--usepixels-ymax', action='store_true',
            help='Use a value in pixels for min brush y')  

    parser.add_argument('-a','--alpha', type=float, default=0.0075,
            help='Paint alpha. Range from 0.0 to 1.0')
    parser.add_argument('--ext', default='.bmp',
            help='File extension for saving painting, default is .bmp')
    
    parser.add_argument('--fail-count', type=int, default=1500,
            help='Maximum number of failed draw attempts to autosave')
    parser.add_argument('--last-saved-count', type=int, default=4000,
            help='Maximum number of drawings (kept or not) to autosave')

    args = parser.parse_args()

    picfile = args.image
    goal = args.goal
    max_width, max_height = max(1, args.xmax), max(1, args.ymax)
    min_width, min_height = max(1, args.xmin), max(1, args.ymin)
    p_alpha = args.alpha
    im_ext = args.ext if args.ext.startswith('.') else '.'+args.ext
    
    max_fail_count = args.fail_count
    max_last_saved_count = args.last_saved_count
    
    if max_fail_count < 0 or max_last_saved_count < 0:
        raise argparse.ArgumentTypeError('Autosave intervals are >=0!')

    try:
        print 'Opening '+picfile+'...'
        im = Image.open(picfile).convert('RGB')
    
        im_name = os.path.basename(picfile)
        sav_name = 'poly_'+im_name+im_ext
    
        im_array = numpy.array(im)
    
        width, height = im.size[0], im.size[1]
        
        if not (args.usepixels_xmin or args.usepixels):
            min_width = width/min_width
        if not (args.usepixels_xmax or args.usepixels):
            max_width = width/max_width
        if not (args.usepixels_ymin or args.usepixels):
            min_height = height/min_height
        if not (args.usepixels_ymax or args.usepixels):
            max_height = height/max_height
    
        if min_width > min_width:
            raise argparse.ArgumentTypeError('Min width excedes min!')
        if min_height > max_height:
            raise argparse.ArgumentTypeError('Min height excedes max!')
        
        if max_width == min_width:
            raise argparse.ArgumentTypeError('Brush min & max x equal!')
        if max_height == min_height:
            raise argparse.ArgumentTypeError('Brush min & max y equal!')
            
        save_path = os.path.join(os.path.split(picfile)[0],sav_name)
    
        if os.path.exists(save_path):
            print 'Save image found, converting it...'
            save_im = Image.open(save_path).convert('RGB')
        else:
            # get average colour and fill new save image with it
            average = map(int,map(round, im_array.mean(1).mean(0)))
            temp = numpy.array([[average]*width]*height,
                               dtype=numpy.uint8)
            save_im = Image.fromarray(temp)

    except IOError, e:
        print 'Problem loading image file!'
        print e
        
    i = 0
    last_saved_count = 0
    fail_count = 0
    results = [None, None]

    remaining = abs_diff(save_im,im)
    paint_image()
    module = False
else:
    i, fail_count, last_saved_count, max_last_saved_count = 0, 0, 0, 50000
    module = True
    
def draw_and_compare():
    global save_im, remaining, fail_count, last_saved_count, retries
    save_im_copy = save_im.copy()

    poly_rect_area = get_rand_rect()

    save_im_crop = save_im.crop(poly_rect_area)
    save_im_crop.load()
    draw_rand_polys(save_im_crop)

    im_crop = im.crop(poly_rect_area)
    save_im_copy_crop = save_im_copy.crop(poly_rect_area)    
    im_crop.load(), save_im_copy_crop.load()

    blended_crop = Image.blend(save_im_copy_crop,
                               save_im_crop, p_alpha)
    blended_crop.load()
    save_im.paste(blended_crop,
                 (poly_rect_area[0],poly_rect_area[1]))

    old_diff = abs_diff(save_im_copy_crop,im_crop)
    new_diff = abs_diff(blended_crop,im_crop)
    
    if new_diff < old_diff:
        remaining -= old_diff-new_diff
        if not module:
            print str(i) + ':\timproved\t' + str(old_diff-new_diff)\
                         + '\tremaining:\t' + str(remaining)
            #autosave
            if fail_count > max_fail_count\
               or last_saved_count > max_last_saved_count:
                save_im.save(save_path)
                last_saved_count = 0
        fail_count=0
    else:
        save_im = save_im_copy
        fail_count +=1

def paint_image():
    try:
        while remaining > goal:
            # run as thread so as to delay any interrupts until done
            dc_thread = Thread(target=draw_and_compare)
            dc_thread.start()
            dc_thread.join()

            i+=1
            last_saved_count+=1
        
    except (KeyboardInterrupt, SystemExit):
        print 'Saving and exiting...'
        print save_path
        save_im.save(save_path)
