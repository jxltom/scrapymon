from flask_template.views.index import index


@index.route('/_')
def index_test():
    return 'success'
