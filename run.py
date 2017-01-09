from config import DevelopmentConfig, ProductionConfig
from flask_template import create_app, db

app = create_app(ProductionConfig)


if __name__ == '__main__':
    '''
    with flask-template.app_context():
        db.create_all()
    '''
    app.run()
