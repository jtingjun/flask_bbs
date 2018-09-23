from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import current_user, csrf_required, new_csrf_token
from models.topic import Topic
from models.board import Board


main = Blueprint('bp_topic', __name__)


@main.route("/")
def index():
    u = current_user()
    return render_template("/index.html", user=u)


@main.route('/<int:id>')
def detail(id):
    m = Topic.get(id)
    return render_template("topic/detail.html", topic=m)


@main.route("/add", methods=["POST"])
@csrf_required
def add():
    form = request.form.to_dict()
    u = current_user()
    m = Topic.add(form, user_id=u.id)
    return redirect(url_for('.detail', id=m.id))


@main.route("/new")
def new():
    board_id = int(request.args.get('board_id'))
    bs = Board.all()
    token = new_csrf_token()
    return render_template("topic/new.html", bs=bs, token=token, bid=board_id)
