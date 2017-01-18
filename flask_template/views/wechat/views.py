from flask_template import wechat_robot


@wechat_robot.handler
def hello(message):
    return 'Hello World!'
