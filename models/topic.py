from sqlalchemy import Integer, Column, UnicodeText, Unicode
from models.base_model import SQLMixin, db
from models.user import User
from models.reply import Reply


class Topic(SQLMixin, db.Model):
    views = Column(Integer, nullable=False, default=0)
    title = Column(Unicode(50), nullable=False)
    content = Column(UnicodeText, nullable=False)
    user_id = Column(Integer, nullable=False)
    board_id = Column(Integer, nullable=False)

    @classmethod
    def add(cls, form, user_id):
        form['user_id'] = user_id
        m = super().new(form)
        return m

    @classmethod
    def get(cls, id):
        m = cls.one(id=id)
        m.views += 1
        m.save()
        return m

    def user(self):
        u = User.one(id=self.user_id)
        return u

    def replies(self):
        ms = Reply.all(topic_id=self.id)
        return ms

    def reply_count(self):
        count = len(self.replies())
        return count

    @classmethod
    def all_current_user_topic(cls, user_id):
        """
        返回所有当前用户创建过的话题
        """
        ms = Topic.all()
        user_topics = []
        for t in ms:
            # 用户id与帖子是否id一致
            if t.user().id == user_id:
                user_topics.append(t)
        # 逆序topics使其排列从最近发表的开始
        user_topics.reverse()
        return user_topics

    @classmethod
    def all_replied_topic(cls, user_id):
        """
        返回所有当前用户回复过的话题
        """
        ms = Topic.all()
        replied_topics = []
        # all_lasted_replies存放当前用户每一个话题下时间最近的一条回复
        all_lasted_replies = []
        for t in ms:
            # replies存放用户在当前话题下所有的回复
            replies = []
            for r in t.replies():
                if r.user().id == user_id:
                    replies.append(r)
            # 对所有当前用户在当前话题下的回复按修改时间降序排序
            if replies:
                replies.sort(key=lambda x: x.updated_time, reverse=True)
                lasted_reply = replies[0]
                all_lasted_replies.append(lasted_reply)
        # 对每一个话题下最近的一条回复按时间降序排列
        all_lasted_replies.sort(key=lambda x: x.updated_time, reverse=True)
        for r in all_lasted_replies:
            # 找到每一条回复对应的话题
            replied_topics.append(cls.one(id=r.topic_id))
        return replied_topics

    def last_reply_user(self):
        """
        返回所有当前话题下最后一个回复的用户，没有的话返回话题作者用户
        """
        replies = [r for r in self.replies()]
        print('replies', replies)
        if replies:
            replies.sort(key=lambda x: x.updated_time, reverse=True)
            last_reply = replies[0]
            return last_reply.user()
        else:
            return self.user()
