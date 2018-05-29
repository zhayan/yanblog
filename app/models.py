from datetime import datetime
from hashlib import md5
from app import db


class Article(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	article_name = db.Column(db.String(), index=True, unique=True) #use to recongnize the article
	title = db.Column(db.String(50))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	author = db.Column(db.String(20))
	category = db.Column(db.String(10))
	abstract = db.Column(db.String(300))
	html_body = db.Column(db.Text)

	def comments_num(self):
	    return len(Comment.query.filter_by(article_id=self.id).order_by(Comment.timestamp.desc()).all())

	def __repr__(self):
		return '<Article {}>'.format(self.title)


class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nickname = db.Column(db.String(20))
	email = db.Column(db.String(120))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	body = db.Column(db.Text)
	article_id = db.Column(db.Integer, db.ForeignKey('article.id'))

	def avatar(self, size):
		digest = md5(self.email.lower().encode('utf-8')).hexdigest()
		return 'https://www.gravatar.com/avatar/{}?indeticon&s={}'.format(
			digest, size)

	def __repr__(self):
		return '<Comment {}>'.format(self.body)
