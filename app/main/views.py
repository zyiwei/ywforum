#coding=utf-8 
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask import render_template,session,redirect,url_for,flash,abort,request,current_app,make_response
import os

from .forms import EditProfileForm,EditProfileAdminForm,PostForm,CommentForm
from .. import db
from ..models import User,Post,Role,Comment,Follow,FollowComments
from . import main
from .. import email,decorators
from werkzeug import secure_filename

from ..decorators import admin_required,permission_required
from ..models import Permission
from flask_login import login_user,current_user,login_required
from flask_sqlalchemy import get_debug_queries



@main.route('/shutdown')
def server_shutdown():
	if not current_app.testing:
		abort(404)
	shutdown=request.environ.get('werkzeug.server.shutdown')
	if not shutdown:
		abort(500)
	shutdown()
	return 'Shutting down...'



@main.route('/',methods=['GET','POST'])
def index():
	form=PostForm()
	if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
		post=Post(header=form.header.data,summary=form.summary.data,body=form.body.data,author=current_user._get_current_object(),role=current_user.role)
		db.session.add(post)
		return redirect(url_for('.index'))
	show_followed='0'
	if current_user.is_authenticated:
		show_followed=request.cookies.get('show_followed')
	else:
		query=Post.query
	if show_followed=='1':
		query=current_user.followed_posts
	elif show_followed=='2':
		query=db.session.query(Post).select_from(User).filter_by(role_id=1).join(Post,User.id==Post.author_id)
	elif show_followed=='3':
		query=current_user.followed_posts.filter(Post.role_id==1)
	elif show_followed=='4':	
		query=db.session.query(Post).select_from(User).filter_by(role_id=2).join(Post,User.id==Post.author_id)
	else:
		query=Post.query
	page=request.args.get('page',1,type=int)
	pagination=query.order_by(Post.timestamp.desc()).paginate(page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
	posts=pagination.items
	return render_template('index.html',form=form,posts=posts,current_time=datetime.utcnow(),pagination=pagination)



@main.route('/replycomments/<username>')
@login_required
def replyComments(username):
	user=User.query.filter_by(username=username).first()
	if user:
		query=Comment.query.filter_by(reply_id=user.id)
		page=request.args.get('page',1,type=int)
		pagination=query.order_by(Comment.timestamp.desc()).paginate(page,per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],error_out=False)
		comments=pagination.items
		return render_template('show_reply_comments.html',username=username,comments=comments,pagination=pagination)
	else:
		abort(404)



@main.route('/user/<username>')
def user(username):
	user=User.query.filter_by(username=username).first()
	if user is None:
		abort(404)
	page=request.args.get('page',1,type=int)
	pagination=Post.query.filter_by(author_id=user.id).order_by(Post.timestamp.desc()).paginate(page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
	posts=pagination.items
	return render_template('user.html',user=user,posts=posts,pagination=pagination)



@main.route('/edit-profile',methods=['GET','POST'])
@login_required
def edit_profile():
	form=EditProfileForm()
	if form.validate_on_submit():
		current_user.name=form.name.data
		current_user.location=form.location.data
		current_user.about_me=form.about_me.data
 
		avatar=request.files['avatar']
		fname=current_user.username+'_'+secure_filename(avatar.filename)
		UPLOAD_FOLDER=os.getcwd()+'/app/static/avatar/'
		ALLOWED_EXTENSIONS=['png','gif','jpeg','jpg']
		flag='.' in fname and fname.rsplit('.',1)[1] in ALLOWED_EXTENSIONS
		if not flag:
			flash('File Type Error!')
			return redirect(url_for('.user',username=current_user.username))
		avatar.save(UPLOAD_FOLDER+fname)
		current_user.avatar='/static/avatar/'+fname
		
		db.session.add(current_user)
		flash('Your profile has been updated.')
		return redirect(url_for('main.user',username=current_user.username))
	form.name.data=current_user.name
	form.location.data=current_user.location
	form.about_me.data=current_user.about_me
	return render_template('edit_profile.html',form=form,user=current_user) 


@main.route('/edit-profile/<int:id>',methods=['GET','POST'])
@login_required
@admin_required
def edit_profile_admin(id):
	user=User.query.get_or_404(id)
	form=EditProfileAdminForm(user=user)
	if form.validate_on_submit():
		user.email=form.email.data
		user.username=form.username.data
		user.confirmed=form.confirmed.data
		user.role=Role.query.get(form.role.data)
		user.name=form.name.data
		user.location=form.location.data
		user.about_me=form.about_me.data

		avatar=request.files['avatar']
		fname=user.username+'_'+secure_filename(avatar.filename)
		UPLOAD_FOLDER=os.getcwd()+'/app/static/avatar/'
		ALLOWED_EXTENSIONS=['png','gif','jpeg','jpg']
		flag='.' in fname and fname.rsplit('.',1)[1] in ALLOWED_EXTENSIONS
		if not flag:
			flash('File Type Error!')
			return redirect(url_for('.user',username=user.username))
		avatar.save(UPLOAD_FOLDER+fname)
		user.avatar='/static/avatar/'+fname

		db.session.add(user)
		db.session.commit()
		flash('The profile has been updated.')
		return redirect(url_for('main.user',username=user.username))
	form.email.data=user.email
	form.username.data=user.username
	form.confirmed.data=user.confirmed
	form.role.data=user.role_id
	form.name.data=user.name
	form.location.data=user.location
	form.about_me.data=user.about_me
	return render_template('edit_profile.html',form=form,user=user)
 


@main.route('/post/<int:id>',methods=['GET','POST'])
def post(id):
	post=Post.query.get_or_404(id)
	form=CommentForm()
	if form.validate_on_submit():
		comment=Comment(body=form.body.data,post=post,author=current_user._get_current_object())
		db.session.add(comment)
		flash('您的评论已成功发表/Your comment has been published.')
		return redirect(url_for('.post',id=post.id,page=-1))
	page=request.args.get('page',1,type=int)
	if page==-1:
		page=(post.comments.count()-1)/current_app.config['FLASKY_POSTS_PER_PAGE']+1
	pagination=post.comments.order_by(Comment.timestamp.asc()).paginate(page,
		per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
	comments=pagination.items
	post.readcount=post.readcount+1
	return render_template('post.html',posts=[post],form=form,comments=comments,pagination=pagination)


@main.route('/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit(id):
	post=Post.query.get_or_404(id)
	if current_user!=post.author and not current_user.can(Permission.ADMINISTER):
		abort(403)
	form=PostForm()
	if form.validate_on_submit():
		post.header=form.header.data
		post.summary=form.summary.data
		post.body=form.body.data
		db.session.add(post)
		flash('文章已更新/The post has been updated.')
		return redirect(url_for('.post',id=post.id))
	form.header.data=post.header
	form.summary.data=post.summary
	form.body.data=post.body
	post.readcount=post.readcount+1
	return render_template('edit_post.html',form=form)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
	user=User.query.filter_by(username=username).first()
	if user is None:
		flash('Invalid user.')
		return redirect(url_for('.index',datetime=datetime.utcnow()))
	if current_user.is_following(user):
		flash('You are already following this user.')
		return redirect(url_for('.user',username=username))
	current_user.follow(user)
	return redirect(url_for('.user',username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
	user=User.query.filter_by(username=username).first()
	if user is None:
		flash('Invalid user.')
		return redirect(url_for('.index',datetime=datetime.utcnow()))
	if not current_user.is_following(user):
		flash('You\'ve not followed this user yet.')
		return redirect(url_for('.user',username=username))
	current_user.unfollow(user)
	return redirect(url_for('.user',username=username))


@main.route('/followers/<username>')
def followers(username):
	user=User.query.filter_by(username=username).first()
	if user is None:
		flash('Invalid user.')
		return redirect(url_for('.index',datetime=datetime.utcnow()))
	page=request.args.get('page',1,type=int)
	pagination=user.followers.paginate(page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
	follows=[{'user':item.follower,'timestamp':item.timestamp} for item in pagination.items]
	return render_template('followers.html',user=user,title="Followers of",endpoint='.followers',
		pagination=pagination,follows=follows)


@main.route('/followed_by/<username>')
def followed_by(username):
	user=User.query.filter_by(username=username).first()
	if user is None:
		flash('Invalid user.')
		return redirect(url_for('.index',datetime=datetime.utcnow()))
	page=request.args.get('page',1,type=int)
	pagination=user.followed.paginate(page,
		per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
		error_out=False)
	follows=[{'user':item.followed,'timestamp':item.timestamp} for item in pagination.items]
	return render_template('followers.html',user=user,title="Followed by",endpoint='.followed_by',
		pagination=pagination,follows=follows)


@main.route('/all')
@login_required
def show_all():
	resp=make_response(redirect(url_for('.index')))
	resp.set_cookie('show_followed','0',max_age=30*24*60*60)
	return resp

@main.route('/followed')
@login_required
def show_followed():
	resp=make_response(redirect(url_for('.index')))
	resp.set_cookie('show_followed','1',max_age=30*24*60*60)
	return resp

@main.route('/all-moderators')
@login_required
def show_all_moderators():
	resp=make_response(redirect(url_for('.index')))
	resp.set_cookie('show_followed','2',max_age=30*24*60*60)
	return resp

@main.route('/followed-moderators')
@login_required
def show_followed_moderators():
	resp=make_response(redirect(url_for('.index')))
	resp.set_cookie('show_followed','3',max_age=30*24*60*60)
	return resp

@main.route('/admin')
@login_required
def show_admin():
	resp=make_response(redirect(url_for('.index')))
	resp.set_cookie('show_followed','4',max_age=30*24*60*60)
	return resp



@main.route('/show_comments/<username>')
@login_required
def show_comments(username):
	user=User.query.filter_by(username=username).first()
	if user is None:
		abort(404)
	comments=Comment.query.filter_by(author_id=user.id).order_by(Comment.timestamp.desc()).all()
	return render_template('user_comments.html',user=user,comments=comments)



@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
	page=request.args.get('page',1,type=int)
	pagination=Comment.query.order_by(Comment.timestamp.desc()).paginate(page,
		per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
	comments=pagination.items
	return render_template('moderate.html',comments=comments,pagination=pagination,page=page)


@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
	comment=Comment.query.get_or_404(id)
	comment.disabled=False
	db.session.add(comment)
	return redirect(url_for('.moderate',page=request.args.get('page',1,type=int)))

@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
	comment=Comment.query.get_or_404(id)
	comment.disabled=True
	db.session.add(comment)
	return redirect(url_for('.moderate',page=request.args.get('page',1,type=int)))
 
@main.route('/delete-comment/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def delete_comment(id):
	comment=Comment.query.get_or_404(id)
	comment.delete()
	db.session.delete(comment)
	db.session.commit()
	flash('该评论已被删除！')
	return redirect(url_for('.moderate',page=request.args.get('page',1,type=int)))

@main.route('/delete-post/<int:id>')
@login_required
def delete_post(id):
	post=Post.query.get_or_404(id)
	post.delete()
	db.session.delete(post)
	db.session.commit()
	flash('该文章已被删除！')
	return redirect(url_for('.index'))

@main.route('/delete-user/<int:id>')
@login_required
@admin_required
def delete_user(id):
	user=User.query.get_or_404(id)
	if user.posts.all():
		for post in user.posts.all():
			post.delete()
			db.session.delete(post)
	user.delete()
	db.session.delete(user)
	db.session.commit()
	flash('该用户已被删除！')
	return redirect(url_for('.moderate_users'))



@main.route('/reply/<int:id>',methods=['GET','POST'])
@login_required
@permission_required(Permission.COMMENT)
def reply(id):
	comment=Comment.query.get_or_404(id)
	post=Post.query.get_or_404(comment.post_id)
	author=comment.author
	form=CommentForm()
	if form.validate_on_submit():
		reComment=Comment(body=form.body.data,post=post,author=current_user._get_current_object())
		reComment.follow(comment)
		reComment.reply_id=comment.author_id
		db.session.add(reComment)
		flash('您的回复已成功发表！')
		post.readcount=post.readcount+1
		return redirect(url_for('.post',id=post.id,page=-1))
	return render_template('reply.html',form=form,author=author)



@main.route('/moderate-users')
@login_required
@admin_required
def moderate_users():
	page=request.args.get('page',1,type=int)
	pagination=User.query.paginate(page,
		per_page=current_app.config['FLASKY_USERS_PER_PAGE'],
		error_out=False)
	users=[{'timestamp':item.last_seen,'id':item.id,'username':item.username,'role':item.role.name,'avatar':item.avatar} for item in pagination.items]
	return render_template('moderate_users.html',endpoint='.moderate_users',
		pagination=pagination,users=users)


@main.after_app_request
def after_request(response):
	for query in get_debug_queries():
		if query.duration>=current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
			current_app.logger.warning(
				'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'%(query.statement,query.parameters,query.duration,query.context))
	return response



