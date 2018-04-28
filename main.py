from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
# Note:  The connection string after :// contains the following info:
# user:password@server:portNumber/databaseName
app.config['SQLALCHEMY-ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(200))

    def __init__(self, name, body):
        self.name = name
        self.body = body


@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    name_error = ''
    body_error = ''
    if request.method == 'GET':
        return render_template('new_post.html')
    
    if request.method == 'POST':
        name = request.form['name']
        body = request.form['body']

        if name == '':
            name_error = "Please enter a name for your blog"
        if body == '':
            body_error = "Please enter your blog"

        if name_error and body_error:
            return render_template('new_post.html', name_error=name_error, body_error=body_error)
        elif name_error:
            return render_template('new_post.html', name_error=name_error, body=body)
        elif body_error:
            return render_template('new_post.html', name=name, body_error=body_error)
        else:
            blog = Blog(name, body)
            db.session.add(blog)
            db.session.commit()
            blog_query = "/blog?id=" + str(blog.id)
            return redirect('/individual_blog?name=' + name + '&body' + body)


@app.route('/individual_blog', methods=['GET'])
def individual_blog():
    name = request.args.get('blog.name')
    body = request.args.get('blog.body')
    return render_template('individual_blog.html', name=name, body=body)


@app.route('/', methods=['POST', 'GET'])
def index():
    all_blogs = Blog.query.all()
    return render_template('blogs.html', title="Build A Blog", all_blogs=all_blogs)


if __name__ =='__main__':
    app.run()