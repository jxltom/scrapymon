from flask_boilerplate.app import wechat


@wechat.filter('_')
def wechat_test():
    return 'success'
