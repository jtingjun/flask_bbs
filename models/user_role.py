from models.base_model import SQLMixin, db
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String


class Role(SQLMixin, db.Model):
    __tablename__ = 'roles'
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """
    role = Column(String(50), nullable=False)
    users = relationship('User', backref='roles')
