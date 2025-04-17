from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer, String


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


# I chose SQLAlchemy as database
db = SQLAlchemy(model_class=Base)


class AddNewCoffee(db.Model):
    __tablename__ = "coffee"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cafe: Mapped[str] = mapped_column(String(50), nullable=False)
    location: Mapped[str] = mapped_column(String(50), nullable=False)
    rating: Mapped[float] = mapped_column(Integer, nullable=False)
    review: Mapped[str] = mapped_column(String(200), nullable=False)
    link: Mapped[str] = mapped_column(String(400), nullable=False)
    img_url: Mapped[str] = mapped_column(String(300), nullable=False)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

