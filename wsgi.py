from config import Config
from flask_template import (create_app, create_worker,
                            register_celery, init_database)

app = create_app(Config(
    bootstrap=True,
    db=True,
    scheduler=True,
    mail=True,
    index=True,
    login=True,
    wechat=True,
))
worker = create_worker(app)
register_celery()
print('import db in wsgi')
from flask_template import db

print(db.Model.metadata.tables)
print('import db in wsgi done')

with app.app_context():
    db.create_all(app=app)
#init_database()

if __name__ == '__main__':
    app.config.update(DEBUG=True)
    app.run()
