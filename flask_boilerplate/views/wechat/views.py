from flask_boilerplate import wechat


@wechat.filter('_')
def wechat_test():
    return 'success'
