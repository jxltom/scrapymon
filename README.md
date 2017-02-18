# flask-boilerplate

A boilerplate for Flask applications.

## Features

- [Bootstrap](http://getbootstrap.com/) and [Flat-UI](https://github.com/designmodo/Flat-UI/) supported by [Flask-Bootstrap](https://github.com/mbr/flask-bootstrap/)
- Database, including MySQL, SQLite, Postgresql and etc., supported by [Flask-SQLAlchemy](https://github.com/mitsuhiko/flask-sqlalchemy)
- [Http basic authentication](https://en.wikipedia.org/wiki/Basic_access_authentication) supported by [Flask-BasicAuth](https://github.com/jpvanhal/flask-basicauth)
- SMTP mail, compatible with asynchronous mode, supported by [Flask-Mail](https://github.com/mattupstate/flask-mail) and Celery
- Task scheduling supported by [APScheduler](https://github.com/agronholm/apscheduler) and [easy-scheduler](https://github.com/jxltom/easy-scheduler)
- Role-based authentication with registration, email confirmation, password recovery, and login tracking, supported by [Flask-Security](https://github.com/mattupstate/flask-security/), [Flask-Login](https://github.com/maxcountryman/flask-login) , [Flask-WTF](https://github.com/lepture/flask-wtf) and [Flask-Principal](https://github.com/mattupstate/flask-principal)                                       
- Administrative interface with authentication supported by [Flask-Admin](https://github.com/flask-admin/flask-admin) and [Flask-Security](https://github.com/mattupstate/flask-security/)
- [Wechat Official Account](https://mp.weixin.qq.com/) supported by [WeRoBot](https://github.com/whtsky/WeRoBot)
- Asynchronous queue supported by [Celery](https://github.com/celery/celery)
- Served by [Gevent](https://github.com/gevent/gevent) for production use
- Wrapper as script or exe with command line arguments support for running as services conveniently
- [Heroku](https://heroku.com/)/[Dokku](https://github.com/dokku/dokku)/[Flynn](https://github.com/flynn/flynn) supported

## Getting Started

- Following environment variables have to be set for using Flask-Mail

    - MAIL_SERVER
    - MAIL_PORT
    - MAIL_USE_TLS
    - MAIL_USE_SSL
    - MAIL_USERNAME
    - MAIL_PASSWORD
    - MAIL_DEFAULT_SENDER
    
- Following environment variables have to be set for using Celery

    - BROKER_URL
    - RESULT_BACKEND
    
- Following environment variable can be set for using different database with ```sqlite:///:memory:```
    
    - SQLALCHEMY_DATABASE_URI

## TODO

- Install dependencies from Github in setup
