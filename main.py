from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'index', 'blog']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in", "success")
            return redirect('/newpost')
        if not username:
            flash('User does not exist', 'error')
        if not password:
            flash('Password is incorrect', 'error')


    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        

        
        existing_user = User.query.filter_by(username=username).first()
          
        if username=='' or password== '' or verify =='':
            flash('One or more fields are invalid. Please fill in all form fields.', 'error')
            return redirect('/signup')

        if len(username) < 3:
            flash('Invalid Username, must be at least 3 characters.', 'error')
            return redirect('/signup')
        
        if len(password) < 3:
            flash('Invalid password, must be at least 3 characters.', 'error')
            return redirect('/signup')

        if verify != password:
            flash('Password and Verify Password fields must match.', 'error')
            return redirect('/signup')
            
        else:
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/newpost')
            else:
                if existing_user.username == username:
                    flash('Username already exists, please choose another username.', 'error')
                    return redirect('/signup')
            
            

    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

@app.route('/', methods= ['POST', 'GET'])
def index():
    users = User.query.order_by(User.id.desc()).all()
    return render_template('index.html', users=users)

@app.route('/blog', methods=['POST', 'GET'])
def blog(): 

    blogs = Blog.query.order_by(Blog.id.desc()).all()
    return render_template('blog.html', blogs=blogs, blog=blog)

   

@app.route('/blog', methods=['POST', 'GET'])
def link_to_individual():
    
    return redirect('/individual')


######FIGURE THIS OUT: HOW TO LINK USERNAME TO SINGLE USER PAGE######
@app.route('/blog')
def link_to_singleUser():
    id = Blog.owner.id
    return redirect('/singleUser?id=' + '{0}'.format(id))
    
    
    
@app.route('/singleUser', methods=["GET", 'POST'])
def singleUser():
    id = request.args.get('id')
    owner = User.query.filter_by(id=id).first()
    blogs = Blog.query.filter_by(owner=owner).all()

    return render_template('singleUser.html', blogs=blogs)
###########################KEEP USER LINK ON SINGLEUSERPAGE###
@app.route('/singleUser')
def stay_on_singleUser():
    id = Blog.owner.id
    return redirect('/singleUser?id=' + '{0}'.format(id))



@app.route('/individual', methods=["GET", 'POST'])
def individual():
    
    
    if request.args:
        id = request.args.get('id')
        blog = Blog.query.filter_by(id=id).first()
        title= Blog.query.filter_by(id=id).first().title
        body= Blog.query.filter_by(id=id).first().body
    

    return render_template('individual.html', blog=blog, title=title, body=body) #owner=owner)

######figure link from blog owner to singleUser page######
@app.route('/individual')
def user_link():
    id = Blog.owner.id
    return redirect('/singleUser?id=' + '{0}'.format(id))
    

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
        return render_template('newpost.html', error=error, title=title, body=body, owner=owner)

    
    else:
        title = request.form['title']
        body = request.form['body']
        owner = User.query.filter_by(username=session['username']).first()  
        new_blog=Blog(title, body, owner)
        db.session.add(new_blog)
        db.session.commit()

        id = new_blog.id
       
        
        return redirect('/individual?id=' + "{0}".format(id))

    



if __name__ == '__main__':
    app.run()