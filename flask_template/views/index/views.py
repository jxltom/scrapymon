from . import index


@index.route('/_')
def index_test():
    return 'success'
