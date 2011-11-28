import pygame
from math import *

def get_fractal_data( complex_rect, size, iters=100 ):
    fractal = pygame.Surface( size )

    for x in xrange(size[0]):
        for y in xrange(size[1]):
            c = ( complex_rect[0][0] + (x * (complex_rect[1][0] - complex_rect[0][0]) / float(size[0])) +
                  complex_rect[0][1] + (y * (complex_rect[1][1] - complex_rect[0][1]) / float(size[1]))*(0.+1.j) )

            z = c
            for n in xrange(iters):
                z = z**2 + c
                if abs(z) >= 2:
                    break
                if is_in_main_body( c ):
                    n = iters-1

            fractal.set_at( (x,y), 
                    pygame.Color( 127*int(1+sin(n)), 127*int(1+cos(n)), 127*int(cos(10*n))) if n < iters-1 else
                    pygame.Color( 0, 0, 0 ) )

    filename = '/tmp/fractal.jpeg'
    pygame.image.save( fractal, filename )
    data = open( filename )
    return data.read()

def is_in_main_body( c ):
    q = (c.real - .25)**2 + c.imag**2
    return (q * (q + (c.real - .25)) < .25 * c.imag ** 2) or ( (c.real + 1)**2 + c.imag**2 < .0625 )

