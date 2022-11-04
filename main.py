from email.policy import default
from msilib import init_database
from flask import Flask, render_template, flash, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from decouple import config
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate

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
migrate = Migrate(app, db)

@app.before_first_request
def create_tables():
    db.create_all()


#models

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('La contraseña no es legible')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    date_added = db.Column(db.DateTime, default=datetime.utcnow)


#create form
class UserForm(FlaskForm):
    name = StringField("Nombre", validators=[DataRequired()]) 
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField("Enviar")
    password_hash = PasswordField('Contraseña', validators=[DataRequired(), EqualTo('password_hash2', message="Contraseñas iguales")])
    password_hash2 = PasswordField('Repetir contraseña', validators=[DataRequired()])
    

@app.route('/')
def index():
    first_name = "raul"
    favorites = ["pepperoni", "cheese", "pineapple"]
    all_users = Users.query.order_by(Users.date_added)
    print(all_users)
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
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(name=form.name.data, 
                            email=form.email.data, 
                            password_hash=hashed_pw
                            )
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.password_hash = ''
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


@app.route('/delete/<int:id>')
def delete_user(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("El usuario se eliminó correctamente")
        all_users = Users.query.order_by(Users.date_added)
        return render_template('delete_user.html')
    
    except:
        flash("Hubo un problema con la borración")
        return render_template('user_add.html', form=form, name=name, our_users=all_users)


@app.route('/spending')
def spend_notes():
    return render_template('spending.html')

@app.route('/clima')
def weather():
    return render_template('weather.html')

if __name__ == '__main__':
    app.run(debug=True)