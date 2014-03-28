import pygame.camera
import sys
import PIL
from PIL import Image
import numpy
from threading import Thread
import SocketServer
import json

import whistler
whistler.im = Image.new("RGB", (1024, 640), "white")
draw_target = whistler.draw_and_compare

import pointillism

class JsonConfigServer(SocketServer.ThreadingTCPServer):
    allow_reuse_address = True

class JsonConfigHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        global draw_target
        config = json.loads(self.request.recv(1024).strip())
        print config
        if config['type'] == 'beziers':
            print 'Changing to beziers'
            whistler.min_width = whistler.im.size[0]/config['min_x']
            whistler.max_width = whistler.im.size[0]/config['max_x']
            whistler.min_height = whistler.im.size[0]/config['min_x']
            whistler.max_height =whistler.im.size[0]/config['max_x']
            draw_target = whistler.draw_and_compare
        elif config['type'] == 'pointillism':
            print 'Changing to Pointillism'
            draw_target = pointillism.draw_and_compare
        self.request.sendall(json.dumps({'return':'ok'}))

server = JsonConfigServer(('127.0.0.1', 8000), JsonConfigHandler)
th = Thread(target=server.serve_forever)
th.daemon = True
th.start()

pygame.init()
pygame.camera.init()

cameras = pygame.camera.list_cameras()
camera = pygame.camera.Camera(cameras[0])

camera.start()
img = camera.get_image()

cam_width = img.get_width()
cam_height = img.get_height()

cam_im_array = pygame.surfarray.array3d(img)#pygame.image.load('sometest.png'))

average = map(int,map(round, cam_im_array.mean(1).mean(0)))
temp = numpy.array([[[0,0,0]]*cam_height]*cam_width,dtype=numpy.uint8)
#temp = numpy.array([[[0,0,0]]*cam_width]*cam_height, dtype=numpy.uint8)                            
whistler.save_im = Image.fromarray(temp)
whistler.im = Image.fromarray(cam_im_array)

whistler.width, whistler.height = cam_height, cam_width#, cam_height

#some defaults
whistler.min_width = cam_width/16
whistler.max_width = cam_width/4
whistler.min_height = cam_height/16
whistler.max_height = cam_height/4
whistler.p_alpha = 0.0125
whistler.remaining = whistler.abs_diff(whistler.save_im, whistler.im)
old_remaining = whistler.remaining

screen = pygame.display.set_mode([cam_width, cam_height])# pygame.FULLSCREEN)
pygame.mouse.set_visible(0)
pygame.display.set_caption("Live Painting")

c = 0
while True :
    for e in pygame.event.get() :
        if e.type == pygame.QUIT\
           or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            pygame.camera.quit()
            sys.exit()
    # try to draw something
    while whistler.fail_count < 1 and whistler.remaining <= old_remaining:
        dc_thread = Thread(target=draw_target)
        dc_thread.start()
        dc_thread.join()
    whistler.fail_count = 0
    old_remaining = whistler.remaining
    if c % 60 == 0:
        img = camera.get_image()
        whistler.im = whistler.im = Image.fromarray(pygame.surfarray.array3d(img))
        whistler.remaining = whistler.abs_diff(whistler.save_im, whistler.im)
    c += 1
    # draw frame
    pygame.surfarray.blit_array(screen, numpy.asarray(whistler.save_im))#.rotate(90)))
    #pygame.surfarray.blit_array(screen, pygame.surfarray.array3d(img))
    #screen.blit(pygame.image.frombuffer(whistler.save_im.tostring(), whistler.save_im.size, whistler.save_im.mode), (0,0))
    
    
    pygame.display.flip()
