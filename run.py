from config import DevelopmentConfig, ProductionConfig
from app import create_app, db

app = create_app(ProductionConfig)


if __name__ == '__main__':
    '''
    with app.app_context():
        db.create_all()
    '''
    app.run()
