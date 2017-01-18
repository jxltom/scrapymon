from flask_template import robot


@robot.handler
def hello(message):
    return 'Hello World!'