from . import index


@index.route('/')
def index_example():
    return 'Hello World'
