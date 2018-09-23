from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    abort,
)
from models.user import User
from models.topic import Topic
from models.board import Board
from routes import current_user, new_csrf_token
import os
import uuid


main = Blueprint('index', __name__)


@main.route("/")
def index():
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.all(board_id=board_id)
    token = new_csrf_token()
    bs = Board.all()
    u = current_user()
    return render_template("topic/index.html", user=u, ms=ms, token=token, bs=bs, bid=board_id)


@main.route("/register", methods=['POST'])
def register():
    form = request.form
    User.register(form)
    return redirect(url_for('.index'))


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    print('login user <{}>'.format(u))
    if u is None:
        return redirect(url_for('bp_topic.index'))
    else:
        session['user_id'] = u.id
        session.permanent = True
        return redirect(url_for('.index'))


@main.route('/profile')
def profile():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        user_topics = Topic.all_current_user_topic(u.id)
        replied_topics = Topic.all_replied_topic(u.id)
        # for t in user_topics:
        #     u = t.last_reply_user()
        #     print('last reply user', u, u.image)
        board_id = int(request.args.get('board_id', -1))
        return render_template('profile.html', user=u, ms=user_topics, rs=replied_topics, bid=board_id)


@main.route('/setting')
def setting():
    u = current_user()
    return render_template('setting.html', user=u)


@main.route('/change_setting', methods=['POST'])
def change_setting():
    form = request.form.to_dict()
    u = current_user()
    # 修改密码
    if 'old_pass' in form:
        old_pass = User.salted_password(form['old_pass'])
        if u.password == old_pass:
            new_pass = User.salted_password(form['new_pass'])
            User.update(u.id, password=new_pass)
    # 更改其它信息
    else:
        print('user_info', form)
        User.update(u.id, **form)
    return redirect(url_for('.profile'))


@main.route('/image/add', methods=['POST'])
def avatar_add():
    file = request.files['avatar']

    suffix = file.filename.split('.')[-1]
    filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
    path = os.path.join('static/avatar/', filename)
    file.save(path)

    u = current_user()
    User.update(u.id, image='/static/avatar/{}'.format(filename))

    return redirect(url_for('.profile'))


@main.route('/user/<int:id>')
def user_detail(id):
    u = User.find(id)
    if u is None:
        abort(404)
    else:
        return render_template('profile.html', user=u)


def not_found(e):
    return render_template('404.html')
