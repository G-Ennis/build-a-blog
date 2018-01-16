from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/blog')
def blog():
    blogs = Blog.query.all()
    return render_template('blog.html', title="Build a Blog", blogs=blogs)

def single_blog():
    blog_id = int(request.args.get('id'))
    blog = Blog.query.filter_by(blog_id)
    return render_template('single_blog.html', title="Current blog", blog=blog)
    


@app.route('/newpost', methods=['GET', 'POST'])
def new_post():
    if request.method == 'GET':
        return render_template('new_post.html')

    if request.method == 'POST':
       
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']
       
        title_error = ''
        body_error = ''

        if blog_title == "":
            title_error = "Please enter a title for your blog"

        if blog_body == "":
            blog_body_error = "Please enter content for your blog"

        if not blog_body_error or title_error:   
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            return render_template('single_blog.html', blog=blog)    


if __name__ == '__main__':
    app.run()

