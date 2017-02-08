from flask_boilerplate import robot


@robot.filter('_')
def wechat_test():
    return 'success'
