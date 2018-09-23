from sqlalchemy import create_engine
import secret
from app import configured_app
from models.base_model import db
from models.topic import Topic
from models.user import User
from models.user_role import Role
from models.board import Board
from models.reply import Reply


def reset_database():
    url = 'mysql+pymysql://root:{}@localhost/?charset=utf8mb4'.format(secret.database_password)
    e = create_engine(url, echo=True)

    with e.connect() as c:
        c.execute('DROP DATABASE IF EXISTS BBS')
        c.execute('CREATE DATABASE BBS CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        c.execute('USE BBS')

    db.metadata.create_all(bind=e)


def generate_fake_data():
    Role.new(dict(role='guest'))
    Role.new(dict(role='normal'))
    guest = dict(
        username='Guest',
        password='',
        image='/static/avatar/guest.jpg',
        role_id=1,
    )
    User.register(guest)

    form1 = dict(
        username='test',
        password='123',
        image='/static/avatar/avatar.jpg',
        signature='No code, no life',
        role_id=2,
    )
    u = User.register(form1)
    form2 = dict(
        username='test2',
        password='1234',
        image='/static/avatar/avatar2.jpg',
        role_id=2,
    )
    User.register(form2)

    board = dict(
        title='all'
    )
    b = Board.new(board)

    with open('markdown_demo.md', encoding='utf8') as f:
        content = f.read()
    topic_form = dict(
        title='markdown demo',
        content=content,
        board_id=b.id,
        user_id=u.id,
    )

    for i in range(10):
        print('begin topic <{}>'.format(i))
        t = Topic.new(topic_form)

        reply_form = dict(
            content='reply test',
            topic_id=t.id,
            user_id=u.id,
        )
        for j in range(5):
            Reply.new(reply_form)


if __name__ == '__main__':
    app = configured_app()
    with app.app_context():
        reset_database()
        generate_fake_data()
