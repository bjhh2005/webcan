from flask import Blueprint, render_template, request, g, redirect, url_for, current_app
from .forms import BlogForm, CommentForm
from models import BlogModel, CommentModel
from exts import db
from decorators import login_required

bp = Blueprint("post", __name__, url_prefix='/post')

"""@bp.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    start = (page - 1) * current_app.config.get('PER_PAGE_COUNT')
    end = start + current_app.config.get('PER_PAGE_COUNT')
    query_obj = BlogModel.query.order_by(BlogModel.create_time.desc())
    total = query_obj.count()
    posts = query_obj.slice(start, end)
    pagination = Pagination(bs_version=4, page=page, total=total, outer_widows=0, inner_widows=2, alignment="center")
    context = {
        "posts": posts,
        "pagination": pagination
    }
    return render_template("index.html", **context)"""


@bp.route('/')
def index():
    if not g.user:
        return redirect(url_for('user.login'))
    blogs = BlogModel.query.order_by(BlogModel.create_time.desc()).all()
    return render_template("index.html", blogs=blogs)

#@bp.route('/bc/public', methods=['GET', 'POST'])
#@login_required
#def public_bc():
#    if request.method == 'GET':
#        return render_template("public_blog.html")
#    else:
#        form = BlogForm(request.form)
#        if form.validate():
#            title = form.title.data
#            content = form.content.data
#            blog = BlogModel(title=title, content=content, author=g.user)
#            db.session.add(blog)
#            db.session.commit()
#            return redirect("/")
        #todo：跳转到本片问答详情页面
#        else:
#            print(form.errors)
#            return redirect(url_for('post.public_bc'))


@bp.route('/bc/public', methods=['GET', 'POST'])
def public_blog():
    if not g.user:
        return redirect(url_for('user.login'))
    if request.method == 'GET':
        return render_template("public_blog.html")
    else:
        form = BlogForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            blog = BlogModel(title=title, content=content, author=g.user)
            db.session.add(blog)
            db.session.commit()
            return redirect("/post")
        else:
            print(form.errors)
            return redirect(url_for('post.public_blog'))


@bp.route("/bc/detail/<bc_id>")
def bc_detail(bc_id):
    blog = BlogModel.query.get(bc_id)
    return render_template("detail.html", blog=blog)


#@bp.post("/comment/public")
#@login_required
#def public_comment(model_id=None):
#    form = CommentForm(request.form)
#    if form.validate():
#        content = form.content.data
#        blog_id = form.blog_id.data
#        comment = CommentModel(content=content, blog_id=blog_id, author_id=g.user.id)
#        db.session.add(comment)
#        db.session.commit()
#        return redirect(url_for('post.bc_detail', bc_id=blog_id))
#    else:
#        print(form.errors)
#        return redirect(url_for('post.bc_detail', bc_id=request.form.get("blog_id")))


@bp.post("/comment/public")
def public_comment(model_id=None):
    if not g.user:
        return redirect(url_for('user.login'))
    form = CommentForm(request.form)
    if form.validate():
        content = form.content.data
        blog_id = form.blog_id.data
        comment = CommentModel(content=content, blog_id=blog_id, author_id=g.user.id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('post.bc_detail', bc_id=blog_id))
    else:
        print(form.errors)
        return redirect(url_for('post.bc_detail', bc_id=request.form.get("blog_id")))


@bp.route("/search")
def search():
    q = request.args.get("q")
    blogs = BlogModel.query.filter(BlogModel.title.contains(q)).all()
    return render_template("index.html", blogs=blogs)