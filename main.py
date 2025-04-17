import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, request, flash
from models import db, User, AddNewCoffee
from forms import CoffeeReviewForm, RegisterForm, LoginForm
from flask_bootstrap import Bootstrap5
from sqlalchemy import Integer, String, or_
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

# I firstly set Flask as backend
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# I need to configure SQLAlchemy with a database URI and initialize it.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coffee.db'
db.init_app(app)
Bootstrap5(app)
login_manager = LoginManager()
login_manager.init_app(app)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    coffees = AddNewCoffee.query.all()
    return render_template('index.html', coffees=coffees)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


@app.route('/register', methods=["GET", "POST"])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        email = register_form.email.data
        password = register_form.password.data
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()
        if user:
            flash("You've already signed up with that email, log in instead!", category="error")
            return redirect(url_for('login'))

        hash_and_salted_pass = generate_password_hash(
            register_form.password.data,
            method="pbkdf2:sha256",
            salt_length=8
        )

        new_user = User(
            email=register_form.email.data,
            password=register_form.password.data,
            name=register_form.name.data
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("home"))

    return render_template("register.html", form=register_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()

        if not user:
            flash("That email does not exist, please try again.", category="error")
            return redirect(url_for('login'))

        elif not check_password_hash(user.password, password):
            flash("Password incorrect, please try again.")
            return redirect(url_for('login'))

        else:
            login_user(user)
            return redirect(url_for('home')) #ここまだ　未定

    return render_template('login.html', form=login_form, logged_in=current_user.is_authenticated)


@app.route('/add_new_coffee', methods=["GET", "POST"])
def add_coffee():
    form = CoffeeReviewForm()
    if form.validate_on_submit():
        # Process form data and save to the database
        new_cafe = AddNewCoffee(
            cafe=form.name.data,
            location=form.location.data,
            rating=form.rating.data,
            review=form.review.data,
            link=form.link.data,
            img_url=form.img_url.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html', form=form)


@app.route('/edit/<int:coffee_id>', methods=["POST", "GET"])
def edit_post(coffee_id):
    post_to_edit = db.get_or_404(AddNewCoffee, coffee_id)
    edit_form = CoffeeReviewForm(
        name=post_to_edit.cafe,
        location=post_to_edit.location,
        rating=post_to_edit.rating,
        review=post_to_edit.review,
        link=post_to_edit.link,
        img_url=post_to_edit.img_url
    )
    if edit_form.validate_on_submit():
        post_to_edit.cafe = edit_form.name.data
        post_to_edit.location = edit_form.location.data
        post_to_edit.rating = edit_form.rating.data
        post_to_edit.review = edit_form.review.data
        post_to_edit.link = edit_form.link.data
        post_to_edit.img_url = edit_form.img_url.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', form=edit_form)


@app.route('/search')
def search():
    query = request.args.get('query')
    if query:
        results = AddNewCoffee.query.filter(
            or_(
                AddNewCoffee.cafe.ilike(f"%{query}%"),
                AddNewCoffee.review.ilike(f"%{query}%"),
                AddNewCoffee.location.ilike(f"%{query}%")
            )
        ) .all()
    else:
        results = []
    return render_template('search_result.html', results=results, query=query)


# これがないと Flask は runしない
if __name__ == '__main__':
    app.run(debug=True)
