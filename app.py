from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    email = db.Column(db.Text, nullable = False)
    password = db.Column(db.Text, nullable = False)

    def __repr__(self):
        return (self.name)


user = ''


@app.route('/home')

def home():
    return render_template('home.html', name = user)



@app.route('/', methods = ['GET', 'POST'])


def login():

    global user

    if request.method == 'POST':

        try_email = request.form['loginEmail']
        try_password = request.form['loginPass']

        try:

            user = Users.query.filter_by(email = try_email).first()

            # return redirect('/')

            if user.email == False:
                    return render_template('login.html', info = 'Invalid Email Id!!')
            elif try_password != user.password:
                    return render_template('login.html', info = 'Invalid Password!!')
            else:
                    return redirect('/home')

        except:
            return render_template('login.html', info = 'Invalid User!!')

    else:

        return render_template('login.html')





@app.route('/create', methods = ['GET', 'POST'])

def create():

    if request.method == 'POST':
        new_name = request.form['newName']
        new_email = request.form['newEmail']
        new_pass = request.form['newPass']
        user = Users(name = new_name, email = new_email, password = new_pass)
        db.session.add(user)
        db.session.commit()

        return redirect('/')
    else:
        return render_template('create.html')



@app.route('/view')

def view():
    return render_template('view.html', name = user)



@app.route('/edit/<int:id>', methods = ['GET', 'POST'])

def edit(id):

    global user

    user = Users.query.get_or_404(id)
    

    if request.method == 'POST':
        user.name = request.form['editName']
        user.email = request.form['editEmail']
        user.password = request.form['editPass']
        db.session.commit()
        return render_template('home.html', name = user)

    else:
        return render_template('edit.html', name = user)



@app.route('/delete/<int:id>')

def delete(id):

    user = Users.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')
        



if __name__ =='__main__':
    app.run(debug = True)