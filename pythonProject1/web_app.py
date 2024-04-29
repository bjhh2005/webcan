from flask import Flask, session, g
from flask_migrate import Migrate
from sqlalchemy.testing.pickleable import User
from flask_moment import Moment
from blueprints.user import bp as user_bp
from blueprints.front_page import bp as front_page_bp
from blueprints.post import bp as post_bp
from flask_login import LoginManager
import config
from exts import db, mail
from models import UserModel

app = Flask(__name__)
# 配置绑定文件
app.config.from_object(config)
moment = Moment(app)

db.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(user_bp)
app.register_blueprint(front_page_bp)
app.register_blueprint(post_bp)


@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)


@app.context_processor
def my_context_processor():
    return {'user': g.user}


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")