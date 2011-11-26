import pygame
from config import *

def get_fractal_data( complex_rect ):
    fractal = pygame.Surface( (WIDTH, HEIGHT) )
    fractal.fill( pygame.Color( 255, 0, 0 ) )
    filename = '/tmp/fractal.jpeg'
    pygame.image.save( fractal, filename )
    data = open( filename )
    return data.read()

