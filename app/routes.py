from flask import render_template, url_for, flash, redirect, request, jsonify
from werkzeug.urls import url_parse
from app import app
from app import db
from app.forms import CommentForm
from app.models import Article, Comment
import string

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def index():
	page = request.args.get('page', 1, type=int)
	posts = Article.query.order_by(Article.timestamp.desc())
	posts = posts.paginate(page, app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('index', page=posts.next_num) \
		if posts.has_next else None
	prev_url = url_for('index', page=posts.prev_num) \
		if posts.has_prev else None
	return render_template('home.html',home='HOME PAGE', 
		posts=posts.items, next_url=next_url, prev_url=prev_url)

@app.route('/article/<article_name>', methods=['GET', 'POST'])
def article(article_name):
	page = request.args.get('page', 1, type=int)
	article = Article.query.filter_by(article_name=article_name).first_or_404()
	category = article.category
	comments = Comment.query.filter_by(article_id=article.id).order_by(Comment.timestamp.desc()).paginate(page, app.config['COMMENTS_PER_PAGE'], False)
	next_url = url_for('article', article_name=article_name, page=comments.next_num) \
		if comments.has_next else None
	prev_url = url_for('article', article_name=article_name, page=comments.prev_num) \
		if comments.has_prev else None
	form = CommentForm()
	if form.validate_on_submit():
		comment = Comment(article_id=article.id, nickname=form.nickname.data, email=form.email.data, body=form.comment.data)
		db.session.add(comment)
		db.session.commit()
		return redirect(url_for('article',article_name=article.article_name)+'#comments')
	return render_template('article.html', category=category, article=article,
	 title='article', form=form, comments=comments.items, next_url=next_url, prev_url=prev_url)

@app.route('/author/<author>')
def author(author):
	page = request.args.get('page', 1, type=int)
	posts = Article.query.filter_by(author=author).order_by(Article.timestamp.desc())
	posts = posts.paginate(page,app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('author', author=author, page=posts.next_num) \
		if posts.has_next else None
	prev_url = url_for('author', author=author, page=posts.prev_num) \
		if posts.has_prev else None
	author = string.capwords(author)
	return render_template("list.html",title=author, author=author, 
		posts=posts.items, next_url=next_url, prev_url=prev_url)

@app.route('/category/<category>')
def category(category):
	page = request.args.get('page', 1, type=int)
	if category == 'all':
		posts = Article.query.order_by(Article.timestamp.desc())
		category = 'all articles'
	else:
		posts = Article.query.filter_by(category=category).order_by(Article.timestamp.desc())
		category = category
	posts = posts.paginate(page,app.config['POSTS_PER_PAGE'], False)
	category = string.capwords(category)
	next_url = url_for('category', category=category, page=posts.next_num) \
		if posts.has_next else None
	prev_url = url_for('category', category=category, page=posts.prev_num) \
		if posts.has_prev else None
	return render_template("list.html",title=category, category=category, 
		posts=posts.items, next_url=next_url, prev_url=prev_url)

@app.route('/resume')
def resume():
	return render_template('resume.html',title='resume')

@app.route('/test/<article_name>')
def test(article_name):
	article = Article.query.filter_by(article_name=article_name).first_or_404()
	html_body = article.html_body
	category = article.category
	return render_template('article.html', category=category, html_body=html_body)


	
