from flask_template import robot


@robot.filter('_')
def wechat_test():
    return 'success'
