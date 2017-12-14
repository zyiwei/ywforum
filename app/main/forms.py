#-*- coding=utf-8 -*-
from flask_wtf import Form
from wtforms import StringField,SubmitField,TextAreaField,BooleanField,SelectField,FileField
from wtforms.validators import Required,Length,Regexp,EqualTo,Email
from ..models import Role,User,Comment,Post
from flask_pagedown.fields import PageDownField


class NameForm(Form):
	name=StringField('What is your name?/你的姓名：',validators=[Required()])
	submit=SubmitField('Submit/提交')


class EditProfileForm(Form):
	name=StringField('Real name/实名:',validators=[Length(0,64)])
	avatar=FileField('avatar/头像:')
	location=StringField('Location/位置:',validators=[Length(0,64)])
	about_me=TextAreaField('About me/关于我:')
	submit=SubmitField('Submit/提交')


class EditProfileAdminForm(Form):
	email=StringField('Email/邮箱:',validators=[Required(),Length(1,64),Email()])
	username=StringField('Username/用户名:',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters, numbers, dots or underscores')])
	confirmed=BooleanField('Confirmed/认证')
	role=SelectField('Role/权限',coerce=int)
	avatar=FileField('Avatar/头像:')
	name=StringField('Real name/实名:',validators=[Length(0,64)])
	location=StringField('Location/位置:',validators=[Length(0,64)])
	about_me=TextAreaField('About me/关于我:')
	submit=SubmitField('Submit/提交')

	def __init__(self,user,*args,**kargs):
		super(EditProfileAdminForm,self).__init__(*args,**kargs)
		self.role.choices=[(role.id,role.name) for role in Role.query.order_by(Role.name).all()]
		self.user=user

	def validate_email(self,field):
		if field.data!=self.user.email and User.query.filter_by(email=field.data).first():
			raise ValidationError('邮箱已注册/Email already registered!')

	def validate_username(self,field):
		if field.data!=self.user.username and User.query.filter_by(username=field.data).first():
			raise ValidationError('此邮箱地址已被使用/Email already in use!')



class PostForm(Form):
	header=StringField("题目:",validators=[Required(),Length(1,50)])
	summary=StringField("摘要:",validators=[Required(),Length(1,200)])
	body=PageDownField("内容:",validators=[Required()])
	submit=SubmitField('Submit/提交')


class CommentForm(Form):
	body=StringField('',validators=[Required()])
	submit=SubmitField('Submit/提交')




	



			