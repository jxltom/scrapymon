from config import Config
from flask_template import create_app


config = Config(debug=False)
config.enable_index_blueprint()
config.enable_login_blueprint()
app = create_app(config)


if __name__ == '__main__':
    app.config['DBBUG'] = True
    app.run()
