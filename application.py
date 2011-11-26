import pygame
from bottle import get, template, response

WIDTH = 800
HEIGHT = 600

@get('/<zoom_path:re:[0-9A-F]*>/')
@get('/<zoom_path:re:[0-9A-F]*>')
def page(zoom_path = ''):
    return template('templates/page.html', zoom_path=zoom_path)

@get('/<zoom_path:re:[0-9A-F]*>.jpg')
@get('/<zoom_path:re:[0-9A-F]*>.jpeg')
def image(zoom_path = ''):

    fractal = pygame.Surface( (WIDTH, HEIGHT) )

    fractal.fill( pygame.Color( 255, 0, 0 ) )
    filename = 'images/%s.jpeg' % zoom_path
    pygame.image.save( fractal, filename )

    response.content_type = 'image/jpeg'

    data = open( filename )
    return data.read()

