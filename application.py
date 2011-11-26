from bottle import get, template

@get('/<zoom_path:re:[0-9A-F]*>')
def page(zoom_path = ''):
    return template('templates/page.html', zoom_path=zoom_path)

