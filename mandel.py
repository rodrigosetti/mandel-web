from __future__ import division
import pygame
from colorsys import hsv_to_rgb
from math import *

def get_fractal_data( complex_rect, size, iters=100 ):
    fractal = pygame.Surface( size )

    for x in xrange(size[0]):
        for y in xrange(size[1]):
            c = complex( complex_rect[0][0] + (x * (complex_rect[1][0] - complex_rect[0][0]) / size[0]),
                         complex_rect[0][1] + (y * (complex_rect[1][1] - complex_rect[0][1]) / size[1]) )

            z = c
            for n in xrange(iters):
                z = z**2 + c
                if abs(z) >= 2:
                    break
                elif is_in_main_body( c ):
                    n = iters-1
                    break

            fractal.set_at( (x,y), 
                    pygame.Color(*( int(k*255) for k in hsv_to_rgb( color(z,n,iters), .5, 1)) ) if n < iters-1 else
                    pygame.Color( 0, 0, 0 ) )

    filename = '/tmp/fractal.jpeg'
    pygame.image.save( fractal, filename )
    data = open( filename )
    return data.read()

def is_in_main_body( c ):
    q = (c.real - .25)**2 + c.imag**2
    return (q * (q + (c.real - .25)) < .25 * c.imag ** 2) or ( (c.real + 1)**2 + c.imag**2 < .0625 )

def color( z, n, iters=100 ):
    return n - log( log ( abs(z) ) / log ( iters ) , 2)

