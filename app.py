import time
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import config
import secret
from models.base_model import db
from models.reply import Reply
from models.topic import Topic
from models.user import User
from utils import log

from routes.index import main as index_routes
from routes.topic import main as topic_routes
from routes.reply import main as reply_routes
from routes.message import main as message_routes
from routes.chatroom import main as chat_routes
from routes.index import not_found
from routes.chatroom import socketio


def count(input):
    log('count using jinja filter')
    return len(input)


def format_time(unix_timestamp):
    f = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(unix_timestamp)
    formatted = time.strftime(f, value)
    return formatted


def configured_app():
    app = Flask(__name__)
    # 设置session的secret_key
    app.secret_key = config.secret_key

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:{}@localhost/BBS?charset=utf8mb4'.format(
        secret.database_password
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    socketio.init_app(app)

    # 注册蓝图
    app.register_blueprint(index_routes)
    app.register_blueprint(topic_routes, url_prefix='/topic')
    app.register_blueprint(reply_routes, url_prefix='/reply')
    app.register_blueprint(message_routes, url_prefix='/mail')
    app.register_blueprint(chat_routes, url_prefix='/chatroom')

    # 注册过滤器
    app.template_filter()(count)
    app.template_filter()(format_time)
    app.errorhandler(404)(not_found)

    admin = Admin(app, name='bbs', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Topic, db.session))
    admin.add_view(ModelView(Reply, db.session))

    return app


if __name__ == '__main__':
    app = configured_app()
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    config = dict(
        debug=True,
        host='localhost',
        port=2000,
    )
    # app.run(**config)
    socketio.run(app, **config)
