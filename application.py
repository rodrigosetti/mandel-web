from __future__ import division
from bottle import get, template, response
from mandel import save_fractal
import pygame, string, os
from config import *

POS = { '0' : (0 , 0 ), '1' : (1 , 0 ), '2': (2, 0 ), '3': (3, 0 ),
        '4' : (0 , 1 ), '5' : (1 , 1 ), '6': (2, 1 ), '7': (3, 1 ),
        '8' : (0 , 2 ), '9' : (1 , 2 ), 'A': (2, 2 ), 'B': (3, 2 ),
        'C' : (0 , 3 ), 'D' : (1 , 3 ), 'E': (2, 3 ), 'F': (3, 3 ) }

FLIP_TABLE = string.maketrans('0123456789ABCEDF', 'CDEF89AB45670123')
ROTATE_TABLE = string.maketrans('0123456789ABCEDF', '048C159D26AE37BF')

def get_boundaries( rect ):
    "return the boundaries of a given space"
    global POS

    boundaries = {}
    x = rect[0][0]
    y = rect[0][1]
    step_x = (rect[1][0] - rect[0][0]) / 4.
    step_y = (rect[1][1] - rect[0][1]) / 4.

    for l in POS:
        boundaries[l] = ( (x + POS[l][0]*step_x, y + POS[l][1]*step_y),
                          (x + (POS[l][0]+1)*step_x, y + (POS[l][1]+1)*step_y))

    return boundaries

def get_boundaries_recursive( rect, path ):
    "return the boundaries of a given space in a given path"

    for l in path:
        rect = get_boundaries( rect )[l]

    return rect

def flip_path(path):
    return path.translate( FLIP_TABLE )

@get('/<zoom_path:re:[0-9A-F]*>/')
@get('/<zoom_path:re:[0-9A-F]*>')
def page(zoom_path = ''):

    boundaries = get_boundaries( ((0,0), (HEIGHT, WIDTH)) )

    img_map = {}
    for l in boundaries:
        nl = string.translate( l , ROTATE_TABLE )
        img_map[nl] = (round(boundaries[l][0][1]),
                      round(boundaries[l][0][0]),
                      round(boundaries[l][1][1]),
                      round(boundaries[l][1][0]) )

    return template('templates/page.html', 
            zoom_path=zoom_path, img_map=img_map,
            width=WIDTH, height=HEIGHT)

@get('/root.jpg')
@get('/root.jpeg')
def root_image():
    return image()

@get('/<zoom_path:re:[0-9A-F]+>.jpg')
@get('/<zoom_path:re:[0-9A-F]+>.jpeg')
def image(zoom_path = ''):

    response.content_type = 'image/jpeg'
    response.set_header('Cache-Control', 'public')

    complex_rect = get_boundaries_recursive( COMPLEX_RECT_MAIN, zoom_path )

    filename = IMAGES_DIR + zoom_path + '.jpeg';

    files = os.listdir( IMAGES_DIR )

    if (zoom_path + '.jpeg') not in files:
        save_fractal( complex_rect, (WIDTH, HEIGHT), ITERS, filename )

        if len( files ) > MAX_FILES:
            os.remove( IMAGES_DIR + max( files, key=len ) )

    data = open( filename )
    return data.read()

