from flask import Flask, render_template
from pip import main

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)