from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    completed = db.Column(db.Boolean)

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/blog', methods=['POST', 'GET'])
def blog(): 

    blogs = Blog.query.order_by(Blog.id.desc()).all()
    return render_template('blog.html', blogs=blogs, blog=blog)

@app.route('/blog', methods=['POST', 'GET'])
def link_to_individual():
    
        return redirect('/individual')

@app.route('/individual', methods=["GET", 'POST'])
def individual():
    
    if request.args:
        id=request.args.get('id')
        title = Blog.query.filter_by(id=id).first().title
        body = Blog.query.filter_by(id=id).first().body


    return render_template('individual.html', title=title, body=body, blog=blog)

@app.route('/newpost')
def new_post():
    
    return render_template('newpost.html')



@app.route('/newpost', methods=['GET', 'POST'])
def send_post():

    title = request.form['title']
    body = request.form['body']
    error = ''
    id = ''

    if title =='' or body =='':
        error='Please fill in all form fields before submitting blog'
        return render_template('newpost.html', error=error, title=title, body=body)

    
    else:
        title = request.form['title']
        body = request.form['body']
        new_blog=Blog(title, body)
        db.session.add(new_blog)
        db.session.commit()

        id = new_blog.id
       
        
        return redirect('/individual?id=' + "{0}".format(id))

    



if __name__ == '__main__':
    app.run()