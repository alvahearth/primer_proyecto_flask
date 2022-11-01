from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = "1234"

#create form
class NamerForm(FlaskForm):
    name = StringField("Nombre", validators=[DataRequired()]) 
    submit = SubmitField("Enviar")

@app.route('/')
def index():
    first_name = "raul"
    favorites = ["pepperoni", "cheese", "pineapple"]
    return render_template('index.html', 
                            first_name=first_name, 
                            favorites=favorites)

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
    form = NamerForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
    return render_template('name.html', name=name, form=form)



if __name__ == '__main__':
    app.run(debug=True)