from flask_ckeditor import CKEditorField
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms import SubmitField
from wtforms import TextAreaField
from wtforms import SelectField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import ValidationError
from wtforms.validators import Regexp
from wtforms.validators import EqualTo
from .models import User
from .custom import CancelField


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[
        DataRequired(message='用户名不能为空'), Length(1, 64)])
    password = PasswordField('密码', validators=[DataRequired(message='请输入密码')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

    def validate_username(self, field):
        if not User.query.filter_by(username=field.data):
            raise ValidationError('用户名不存在')


class ResetPasswordForm(FlaskForm):
    username = StringField('用户名', validators=[
        DataRequired(message='用户名不能为空'),
        Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '用户名只能由字母，数字，小数点和下划线组成')])
    old_password = PasswordField('旧密码', validators=[
        DataRequired(message='密码不能为空')])
    password = PasswordField('新密码', validators=[
        DataRequired(message='密码不能为空'), EqualTo('password2', message='密码不一致')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('确认修改')
    cancel = CancelField('取消')

    def validate_old_password(self, field):
        if not current_user.verify_password(field.data):
            raise ValidationError('密码不正确')

    # def validate_username(self, field):
    #     if User.query.filter_by(username=field.data).first():
    #         raise ValidationError('用户名已存在')


class EditorForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired('内容不能空')])
    body = CKEditorField('内容', validators=[DataRequired()])
    mark = StringField('标签')
    category = SelectField('分类', coerce=int, choices=[(1, '学习'), (2, '扯淡')])
    submit = SubmitField('提交')
    cancel = CancelField('取消')


class EditorAboutForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired('内容不能空')])
    body = TextAreaField('内容', validators=[DataRequired('内容不能空')])
    submit = SubmitField('提交')
    cancel = CancelField('取消')
