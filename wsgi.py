from config import Config
from web_scheduler import create_app


config = Config(debug=False)
config.enable_index_blueprint()
config.enable_login_view()
app = create_app(config)


if __name__ == '__main__':
    app.config['DBBUG'] = True
    app.run()
