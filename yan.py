from app import app,db
from app.models import Article, Comment

@app.shell_context_processor
def maeke_shell_context():
	return {'db': db, 'Article': Article, 'Comment': Comment}