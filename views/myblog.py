# coding=utf-8
import datetime
import random
from flask_login import login_user, logout_user, login_required, current_user
from . import main, db
from flask import render_template, flash, redirect, request, url_for
from models import User, Blog
from form import LoginForm, ResetPasswordForm, EditorForm


@main.app_errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


@main.app_errorhandler(503)
def page_not_found(e):
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
		user = User.query.filter_by(username=form.username.data, is_deleted=False).first()
		if user and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			flash('登陆成功')
			if form.password.data == 'admin':
				flash('请更换密码')
				return redirect(url_for('main.reset'))
			return redirect(request.args.get('next', '/') if request.args.get('next') != '/logout' else '/')
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
	blogs = Blog.query.filter_by(is_deleted=False).filter(Blog.mark.like('%' + tag + '%')).all()
	return render_template('index.html', blogs=blogs)


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


@main.route('/fileupload')
@login_required
def file_upload():
	return


@main.route('/publish', methods=['GET', 'POST'])
@login_required
def publish():
	form = EditorForm()
	if form.validate_on_submit():
		blog = Blog(title=form.title.data, body=form.body.data, mark=form.mark.data, author_id=current_user.id)
		db.session.add(blog)
		return redirect(url_for('main.index'))
	return render_template('publish.html', form=form)


@main.route('/details/<int:blog_id>', methods=['GET', 'POST'])
def details(blog_id):
	blog = Blog.query.get_or_404(blog_id)
	return render_template('details.html', blog=blog)
