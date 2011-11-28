from __future__ import division
from bottle import get, template, response
from mandel import save_fractal
import pygame, string, os
from config import *

POS = { '0' : (0 , 0 ), '1' : (0 , 1 ), '2': (0, 2 ), '3': (0, 3 ),
        '4' : (1 , 0 ), '5' : (1 , 1 ), '6': (1, 2 ), '7': (1, 3 ),
        '8' : (2 , 0 ), '9' : (2 , 1 ), 'A': (2, 2 ), 'B': (2, 3 ),
        'C' : (3 , 0 ), 'D' : (3 , 1 ), 'E': (3, 2 ), 'F': (3, 3 ) }

FLIP_TABLE = string.maketrans('0123456789ABCEDF', 'CDEF89AB45670123')

def get_boundaries( rect ):
    "return the boundaries of a given space"
    global POS

    boundaries = {}
    x = rect[0][0]
    y = rect[0][1]
    step_x = (rect[1][0] - rect[0][0]) / 4.
    step_y = (rect[1][1] - rect[0][1]) / 4.

    for l in POS:
        boundaries[l] = ( (y + POS[l][1]*step_y, x + POS[l][0]*step_x),
                          (y + (POS[l][1]+1)*step_y, x + (POS[l][0]+1)*step_x))

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

    img_map = get_boundaries( ((0,0), (HEIGHT, WIDTH)) )

    for l in img_map:
        img_map[l] = (round(img_map[l][0][0]),
                      round(img_map[l][0][1]),
                      round(img_map[l][1][0]),
                      round(img_map[l][1][1]) )

    return template('templates/page.html', 
            zoom_path=zoom_path, img_map=img_map,
            width=WIDTH, height=HEIGHT)

@get('/<zoom_path:re:[0-9A-F]*>.jpg')
@get('/<zoom_path:re:[0-9A-F]*>.jpeg')
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

