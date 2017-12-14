#-*- coding=utf-8 -*-
from flask_wtf import Form
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required,Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(Form):
	email=StringField('Email/邮箱:',validators=[Required(),Length(1,64),Email()])
	password=PasswordField('Password/密码:',validators=[Required()])
	remember_me=BooleanField('keep logged in')
	submit=SubmitField('Log In/登陆')
	

class RegistrationForm(Form):
	email=StringField('Email/邮箱:',validators=[Required(),Length(1,64),Email()])
	username=StringField('Username/用户名:',validators=[Required(),Length(1,64),
					Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters, numbers, dots or underscores')])
	password=PasswordField('Password/密码:',validators=[Required(),EqualTo('password2',message='Passwords must match.')])
	password2=PasswordField('Confirm password/确认密码:',validators=[Required()])
	submit=SubmitField('Register/注册')

	def validate_email(self,field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.')

	def validate_username(self,field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('username already in use.')


class ChangePasswordForm(Form):
	old_password=PasswordField('Old password/原始密码:',validators=[Required()])
	password=PasswordField('New password/新密码:',validators=[Required(),EqualTo('password2',message='Password must match')])
	password2=PasswordField('Confirm new password/确认新密码:',validators=[Required()])
	submit=SubmitField('Update Password/更改密码')


class PasswordResetRequestForm(Form):
	email=StringField('Email/邮箱:',validators=[Required(),Length(1,64),Email()])
	submit=SubmitField('Reset Password/重置密码')


class PasswordResetForm(Form):
	email=StringField('Email/邮箱:',validators=[Required(),Length(1,64),Email()])
	password=PasswordField('New Password/新密码:',validators=[Required(),EqualTo('password2',message='Password must match')])
	password2=PasswordField('Confirm Password/确认新密码',validators=[Required()])
	submit=SubmitField('Reset Password/重置密码')

	def validate_email(self,field):
		if User.query.filter_by(email=field.data).first() is None:
			raise ValidationError('Unknown email address')


class ChangeEmailForm(Form):
	email=StringField('New Email/新邮箱:',validators=[Required(),Length(1,64),Email()])
	password=PasswordField('Password/密码:',validators=[Required()])
	submit=SubmitField('update Email Address/更新邮箱地址')

	def validate_email(self,field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.')






