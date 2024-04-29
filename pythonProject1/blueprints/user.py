import random
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash, abort
from flask_wtf import form
from sqlalchemy.sql.functions import current_user
from sqlalchemy.testing.pickleable import User
from werkzeug.security import generate_password_hash, check_password_hash
from decorators import login_required
from exts import mail, db
from flask_mail import Message
import string
from models import EmailCaptchaModel, UserModel, BlogModel
from .forms import RegisterForm, LoginForm, EditProfileForm, ChangeForm

__package__ = 'blueprints'

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login1.html")
    else:
        form = LoginForm(request.form)
        # 检查格式
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            # 检查是否存在该用户
            if not user:
                flash("用户未找到")
                return redirect(url_for("user.login"))
            # 检查密码
            if check_password_hash(user.password, password):
                 session["user_id"] = user.id
                 return redirect(url_for("front_page.fpage"))
            else:
                flash("密码错误")
                return redirect(url_for("user.login"))
        else:
            flash("表单错误：" + str(form.errors))
            return redirect(url_for("user.login"))


# GET:从服务器上获取数据
# POST：将客户端的数据提交给服务器
@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register4.html")
    else:
        # 验证用户提交的邮箱和验证码是否对应且正确
        # 表单验证：flask-wtf
        form = RegisterForm(request.form)
        # 验证成功，创建用户
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(username=username, email=email, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user.login"))
        # 注册失败
        else:
            print(form.errors)
            return redirect(url_for("user.register"))


@bp.route("/captcha/email", methods=["GET"])
def get_email_captcha():
    try:
        email = request.args.get("email") #获取注册用户邮箱
        #生成验证码
        source = string.digits*4
        captcha = random.sample(source, 4)
        captcha = "".join(captcha)
        #发送验证码给注册用户
        message = Message(subject="您的注册码", recipients=[email], body=f"您的验证码是{captcha}")
        mail.send(message)
        print(captcha)
        #将验证码存入数据库
        email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
        db.session.add(email_captcha)
        db.session.commit()
        return jsonify({"code": 200, "message": "验证码已发送", "data": None})
    except Exception as e:
        return jsonify({"code": 500, "message": str(e), "data": None})


@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@bp.route("/view/<username>")
def view(username):
    user = UserModel.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(BlogModel.create_time.desc()).all()
    return render_template('user.html', user=user)


# 用户级别的资料编辑器
@bp.route("/edit/<username>", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash("您的资料已修改")
        return redirect(url_for("user.view"))
    form.name.data = current_user.username
    form.location.data = current_user.location
    form.about.me = current_user.about_me
    return render_template("edit_profile.html", form=form)


@bp.route("/change_password", methods=["GET", "POST"])
def change_password():
    if request.method == "GET":
        return render_template("change_password.html")
    else:
        form = ChangeForm(request.form)
        if form.validate():
            user = UserModel.query.filter_by(email=form.email.data).first()
            password = form.password.data
            user.password = generate_password_hash(password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user.login"))
        else:
            print(form.errors)
            return redirect(url_for("user.change_password"))

