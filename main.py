import email
from email.policy import default
from msilib import init_database
from django.shortcuts import render
from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from decouple import config

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config('SECRET_KEY')
    return app

def create_db(app):
    #Sqlite db
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/tekke/OneDrive/Escritorio/programs/curso-python/archivos_flask/flask_03/users.db'

    #MySQL db
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/users'


    db = SQLAlchemy(app)
        
    return db
    
app = create_app()
db = create_db(app)

@app.before_first_request
def create_tables():
    db.create_all()


#models

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)


#create form
class UserForm(FlaskForm):
    name = StringField("Nombre", validators=[DataRequired()]) 
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField("Enviar")
    

@app.route('/')
def index():
    first_name = "raul"
    favorites = ["pepperoni", "cheese", "pineapple"]
    all_users = Users.query.order_by(Users.date_added)
    return render_template('index.html', 
                            first_name=first_name, 
                            favorites=favorites,
                            all_users=all_users)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

#invalid URL
@app.errorhandler(404)
def page_not_foung(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_foung(e):
    return render_template('500.html'), 500

@app.route('/name', methods=["GET", "POST"])
def name():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
        flash("Creaste el usuario")
    return render_template('name.html', name=name, form=form)


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
    flash(f"Creaste el usuario { name }")
    
    our_users = Users.query.order_by(Users.date_added)
    return render_template('user_add.html', form=form, name=name, our_users=our_users)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        try:
            db.session.commit()
            flash('Actuliaste correctamente')
            return render_template('user_add.html')
        except:
            flash('Error')
            return render_template('update.html',
                form=form,
                name_to_update=name_to_update
            )
    else:
        return render_template('update.html',
                form=form,
                name_to_update=name_to_update
            )


@app.route('/spending')
def spend_notes():
    return render_template('spending.html')

@app.route('/clima')
def weather():
    return render_template('weather.html')

if __name__ == '__main__':
    app.run(debug=True)