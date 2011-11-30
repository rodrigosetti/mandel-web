from __future__ import division
from PIL import Image, ImageDraw
from colorsys import hsv_to_rgb
from math import *

def save_fractal( complex_rect, size, iters, filename ):
    image = Image.new( 'RGB', size )
    fractal = ImageDraw.Draw(image)

    has_outter = False
    has_inner = False

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

            if n < iters-1:
                has_outter = True
                smooth = color(z,n,iters)
                fractal.point( (x,y), 
                    tuple( int(k*255) for k in hsv_to_rgb( 
                        smooth/100, (sin(smooth/5) + 1)/2, 1)) )
            else:
                has_inner = True
                fractal.point( (x,y), ( 0, 0, 0 ))

    del fractal
    image.save( filename, "JPEG" )

    return has_outter and has_inner

def is_in_main_body( c ):
    "Mandelbrot optimization: returns True if c is within main cardioid or period-1 bulb"
    q = (c.real - .25)**2 + c.imag**2
    return (q * (q + (c.real - .25)) < .25 * c.imag ** 2) or ( (c.real + 1)**2 + c.imag**2 < .0625 )

def color( z, n, iters=100 ):
    "Uses smoth coloring algorithm to get a smooth scale"
    return n - log( log ( abs(z) ) / log ( iters ) , 2)

