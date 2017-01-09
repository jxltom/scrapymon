from config import Config
from flask_template import create_app

config = Config()
config.enable_index_view()
config.enable_login_view()
app = create_app(config)


if __name__ == '__main__':
    app.run()
