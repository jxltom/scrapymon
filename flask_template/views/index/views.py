from . import index


@index.route('/')
def index():
    return 'Hello World'
