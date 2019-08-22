from flask import Flask, render_template, url_for, flash, redirect
from forms import InputForm
from b2i import b2i

app = Flask(__name__)

app.config['SECRET_KEY'] = '23eb28c448bc3cafa6fafe968fa66322'

posts = [
    {
        'author': 'Brad Engberg',
        'title': 'Using Templates',
        'content': 'This is the content',
        'date': '3/20/1980',
    },
    {
        'author': 'Brad Engberg',
        'title': 'Title2',
        'content': 'This is more content',
        'date': '3/20/1981',
    }
]

bindInput = 'this is the input text'

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@app.route('/home/', methods=['GET', 'POST'])
def home():
    form=InputForm()
    if form.validate_on_submit():
        flash("Recieved " + form.bind.data)
    return render_template('home.html', form=form, title='Home')

@app.route('/about')
@app.route('/about/')
def about():
    return render_template('about.html', title='About')

@app.route('/hello/<name>')
def hello(name):
    return render_template('name.html', name=name)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account Created for ' + form.username.data + '!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form) 

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')