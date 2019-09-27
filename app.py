from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from decouple import config
from scipy.sparse import bsr_matrix
from joblib import load

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(app)

nn = load('nearestneighbor_smaller.joblib')
tfidf = load('tfidf (1).joblib')

class Book(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    webpage = DB.Column(DB.BigInteger)
    title = DB.Column(DB.String(300))
    author = DB.Column(DB.String(100))
    descrip = DB.Column(DB.String(25000))
    rating = DB.Column(DB.Float)
    num_ratings = DB.Column(DB.String(30))
    num_reviews = DB.Column(DB.String(30))
    isbn = DB.Column(DB.String(110))
    isbn13 = DB.Column(DB.String(110))
    binding = DB.Column(DB.String(100))
    edition = DB.Column(DB.String(125))
    num_pages = DB.Column(DB.String(100))
    published_on = DB.Column(DB.String(150))
    genres = DB.Column(DB.String(300))

    def __repr__(self):
        return f'Book: {self.title} writtien by {self.author}'


@app.route('/api/description', methods=['POST'])
def api():
    if request.method == 'POST':
        description = request.get_json('description')['description']
        post = tfidf.transform([description])
        #print(post)
        post = bsr_matrix.todense(post)
       # print(post)
        pred_array = nn.kneighbors(post)
        #print(pred_array)
        output = []
        for pred in pred_array[1][0]:
            book = DB.session.query(Book.title, Book.author, Book.rating, Book.isbn).filter(Book.id==int(pred)).all()[0]
            output.append(book)
        return str(pred_array[1][0])

if __name__ == '__main__':
    app.run(debug=True)