from . import index


@index.route('/')
def index_():
    return 'Hello World'
