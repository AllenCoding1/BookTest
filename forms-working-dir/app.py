from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:password@database-test.cxme8k0ioguk.us-east-2.rds.amazonaws.com/flask_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'password'

db = SQLAlchemy(app)

# Book Model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    year_published = db.Column(db.Integer, nullable=True)

# Create tables
with app.app_context():
    db.create_all()

#Main Route
@app.route('/')
def index():
    books = Book.query.all()
    return render_template('list_books.html', books=books)

# Add Book Route
@app.route("/add-book", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        price = request.form['price']
        year_published = request.form['year_published']

        if not title or not author or not price:
            flash('Title, Author, and Price are required fields.', 'error')
            return redirect(url_for('add_book'))

        try:
            new_book = Book(title=title, author=author, price=price, year_published=year_published)
            db.session.add(new_book)
            db.session.commit()
            flash('Book added successfully!')
            return redirect(url_for('get_books'))
        
        except Exception as e:
            flash(f'Error adding book: {str(e)}', 'error')
            return redirect(url_for('add_book'))
    
    return render_template("add_book.html")
# Update Book Route
@app.route("/update-book/<int:id>", methods=["GET", "POST"])
def update_book(id):
    book = Book.query.get_or_404(id)

    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        price = request.form['price']
        year_published = request.form['year_published']

        if not title or not author or not price or not year_published:
            flash('All fields are required!', 'error')
            return redirect(url_for('update_book'))
        try:
            book.title = title
            book.author = author
            book.price = price
            book.year_published = year_published

            db.session.commit()
            flash('Book updated succedssfully!')
            return redirect(url_for('get_books'))
        except Exception as e:
            flash(f'Error updating book: {str(e)}', 'error')
            return redirect(url_for('update_book', id=id))
    return render_template("update_book.html", book=book)

   

#Delete Book Route
@app.route("/delete-book/<int:id>")
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully!')
    return redirect(url_for('get_books'))
#Get books
@app.route("/books", methods=["GET"])
def get_books():
    books = Book.query.all()
    return render_template("list_books.html", books=books)
