from werobot import WeRoBot
robot = WeRoBot()


@robot.handler
def hello(message):
    return 'Hello World!'
