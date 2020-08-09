import random
import datetime
import os
import imghdr
from flask import render_template
from flask import flash
from flask import redirect
from flask import request
from flask import url_for
from flask import abort
from flask import current_app
from flask import make_response
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from flask_login import current_user
from . import main
from . import db
from .models import User
from .models import Blog
from .form import LoginForm
from .form import ResetPasswordForm
from .form import EditorForm
from .form import EditorAboutForm


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.app_errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@main.route('/api')
def api():
    return render_template('api.html')


@main.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            username=form.username.data, is_deleted=False).first()
        if user and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('登陆成功')
            if form.password.data == 'admin':
                flash('请更换密码')
                return redirect(url_for('main.reset'))
            return (redirect(request.args.get('next', '/')
                    if request.args.get('next') != '/logout' else '/'))
        flash('登录失败')
    return render_template('login.html', form=form)


@main.route('/logout', methods=['GET', 'POST'])
def logout():
    if current_user:
        logout_user()
        flash('已退出')
    return redirect(url_for('main.index'))


@main.route('/', defaults={'tag': ''})
@main.route('/<string:tag>')
def index(tag):
    page = request.args.get('page', 1, type=int)
    pagination = Blog.query.filter_by(is_deleted=False).filter(
        Blog.mark.like('%' + tag + '%')).order_by(
            Blog.changed_time.desc()).paginate(
                page,
                per_page=current_app.config['FLASKY_PER_PAGE'],
                error_out=False)
    blogs = pagination.items
    return render_template('index.html', blogs=blogs, pagination=pagination)


@main.route('/learn')
def learn():
    page = request.args.get('page', 1, type=int)
    pagination = Blog.query.filter_by(
        is_deleted=False, category=1).order_by(
            Blog.changed_time.desc()).paginate(
                page,
                per_page=current_app.config['FLASKY_PER_PAGE'],
                error_out=False)
    learn_blogs = pagination.items
    return render_template('index.html',
                           blogs=learn_blogs,
                           pagination=pagination)


@main.route('/blah')
def blah():
    page = request.args.get('page', 1, type=int)
    pagination = Blog.query.filter_by(is_deleted=False, category=2).order_by(
        Blog.changed_time.desc()).paginate(
            page,
            per_page=current_app.config['FLASKY_PER_PAGE'],
            error_out=False)
    blah_blogs = pagination.items
    return render_template('index.html',
                           blogs=blah_blogs,
                           pagination=pagination)


@main.route('/about')
def about():
    blog = Blog.query.filter_by(is_deleted=False, category=0).first()
    if blog:
        return render_template('about.html', blog=blog)
    abort(404)


@main.route('/reset', methods=['GET', 'POST'])
@login_required
def reset():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.password = form.password.data
        flash('密码修改成功')
        return redirect(url_for('main.index'))
    return render_template('reset.html', form=form)


def rand_filename():
    filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '{}{}'.format(filename, str(random.randrange(100, 1000)))


@main.route('/browser', methods=['GET', 'POST'])
@login_required
def browser():
    urls = []
    pics = ['rgb', 'gif', 'pbm', 'pgm', 'ppm', 'tiff',
            'rast', 'xbm', 'jpeg', 'bmp', 'png', 'exif']
    file_path = current_app.static_folder + '/upload'
    object_dir = os.path.dirname(os.path.realpath(__file__))
    for path, dirs, files in os.walk(file_path):
        for f in files:
            url = url_for('static', filename='%s/%s' % ('upload', f))
            file_full_path = object_dir + '/..' + url
            if imghdr.what(file_full_path) in pics:
                urls.append(url)
    return render_template('browser.html', urls=urls)


@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    pics = ['rgb', 'gif', 'pbm', 'pgm', 'ppm', 'tiff',
            'rast', 'xbm', 'jpeg', 'bmp', 'png', 'exif']
    error = ''
    url = ''
    callback = request.args.get("CKEditorFuncNum")
    if request.method == 'POST' and 'upload' in request.files:
        file_obj = request.files['upload']
        if imghdr.what(file_obj) in pics:
            file_name, fext = os.path.splitext(file_obj.filename)
            rnd_name = '{}{}'.format(rand_filename(), fext)
            file_path = os.path.join(
                current_app.static_folder, 'upload', rnd_name)
            dir_name = os.path.dirname(file_path)
            if not os.path.exists(dir_name):
                try:
                    os.makedirs(dir_name)
                except OSError:
                    error = '无法创建目录'
            elif not os.access(dir_name, os.W_OK):
                error = '目录无法写入'
            if not error:
                file_obj.save(file_path)
                url = url_for(
                    'static', filename='%s/%s' % ('upload', rnd_name))
        else:
            error = '请上传图片'
    else:
        error = '上传错误'
    res = """<script type="text/javascript">window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');</script>""" % (
        callback, url, error)
    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response


@main.route('/publish', methods=['GET', 'POST'])
@login_required
def publish():
    form = EditorForm()
    if form.validate_on_submit():
        blog = Blog(title=form.title.data,
                    body=form.body.data,
                    mark=form.mark.data,
                    author_id=current_user.id,
                    category=form.category.data)
        db.session.add(blog)
        return redirect(url_for('main.index'))
    return render_template('editor.html', form=form)


@main.route('/edit/<int:blog_id>', methods=['GET', 'POST'])
@login_required
def edit(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    # if blog.is_deleted:
    #       abort(404)
    form = EditorForm()
    if form.validate_on_submit():
        blog.title = form.title.data
        blog.body = form.body.data
        blog.mark = form.mark.data
        blog.category = form.category.data
        blog.changed_time = datetime.datetime.now()
        blog.changed_user_id = current_user.id
        return redirect(url_for('main.details', blog_id=blog_id))
    form.title.data = blog.title
    form.body.data = blog.body
    form.category.data = blog.category
    if blog.mark:
        form.mark.data = blog.mark
    return render_template('editor.html', form=form)


@main.route('/edit_about', methods=['GET', 'POST'])
@login_required
def edit_about():
    blog = Blog.query.filter_by(is_deleted=False, category=0).first()
    form = EditorAboutForm()
    if form.validate_on_submit():
        blog.title = form.title.data
        blog.body = form.body.data
        blog.changed_time = datetime.datetime.now()
        blog.changed_user_id = current_user.id
        return redirect(url_for('main.about'))
    form.title.data = blog.title
    form.body.data = blog.body
    return render_template('edit_about.html', form=form)


@main.route('/details/<int:blog_id>', methods=['GET', 'POST'])
def details(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    if blog.is_deleted and current_user.is_anonymous:
        abort(403)
    return render_template('details.html', blog=blog)


@main.route('/delete/<int:blog_id>', methods=['GET', 'POST'])
@login_required
def delete(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    if blog.is_deleted:
        abort(404)
    blog.is_deleted = 1
    blog.deleted_time = datetime.datetime.now()
    return redirect(url_for('main.index'))


@main.route('/deleted', methods=['GET', 'POST'])
@login_required
def deleted():
    page = request.args.get('page', 1, type=int)
    pagination = Blog.query.filter_by(is_deleted=1).order_by(
        Blog.deleted_time.desc()).paginate(
            page,
            per_page=current_app.config['FLASKY_PER_PAGE'],
            error_out=False)
    blogs = pagination.items
    return render_template('index.html', blogs=blogs, pagination=pagination)


@main.route('/restore/<int:blog_id>', methods=['GET', 'POST'])
@login_required
def restore(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    if not blog.is_deleted:
        abort(404)
    blog.is_deleted = 0
    return redirect(url_for('main.index'))
