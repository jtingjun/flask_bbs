import hashlib
from sqlalchemy import Column, String, Integer, ForeignKey
from models.base_model import SQLMixin, db
from models.user_role import Role


class User(SQLMixin, db.Model):
    __tablename__ = 'users'

    username = Column(String(50), nullable=False)
    password = Column(String(256), nullable=False)
    image = Column(String(100), nullable=False, default='/static/avatar/guest.jpg')
    signature = Column(String(100), nullable=False, default='这家伙很懒，什么个性签名都没有留下')
    role_id = Column(Integer, ForeignKey('roles.id'), default=2)

    @staticmethod
    def salted_password(password, salt='$!@><?>HUI&DWQa`'):
        salted = hashlib.sha256((password + salt).encode('ascii')).hexdigest()
        return salted

    @classmethod
    def register(cls, form):
        if type(form) != dict:
            form = form.to_dict()
        name = form.get('username', '')
        print('register', form)
        if len(name) > 2 and User.one(username=name) is None:
            form['password'] = User.salted_password(form['password'])
            u = User.new(form)
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        query = dict(
            username=form['username'],
            password=User.salted_password(form['password']),
        )
        print('validate_login', form, query)
        return User.one(**query)
