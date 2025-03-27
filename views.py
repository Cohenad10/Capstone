from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os

# Import models and scraper
from models import db, User, Product, NewsArticle
from scrapers.car_news_scraper import fetch_car_news

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Initialize extensions
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ------------------ LOGIN MANAGER ------------------

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ------------------ ROUTES ------------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shop')
def shop():
    products = Product.query.all()
    return render_template('shop.html', products=products)

@app.route('/news')
def news():
    fetch_car_news()  # Updates on every visit (can be improved later)
    articles = NewsArticle.query.order_by(NewsArticle.date_scraped.desc()).all()
    return render_template('news.html', articles=articles)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:
            login_user(user, remember=True)
            return redirect(url_for('home'))
        flash("Login failed. Try again.")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_user = User(
            username=request.form['username'],
            password=request.form['password'],
            email=request.form['email']
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/contact')
def contact():
    return render_template('contact.html')

# ------------------ INITIAL SETUP ------------------

if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists('database.db'):
            db.create_all()
            db.session.add_all([
                Product(name="Tuning Sticker", price=4.99, description="Gloss vinyl sticker.", stock=100, category="merch"),
                Product(name="Cold Air Intake", price=199.99, description="Universal performance intake.", stock=10, category="parts"),
            ])
            db.session.commit()

    app.run(debug=True, port=8000)
