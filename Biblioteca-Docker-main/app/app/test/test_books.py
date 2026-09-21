from app import db
from app.models.books import Book

def test_index(client):
    response = client.get('/Book/')
    assert response.status_code == 200
    assert b"Libros" in response.data  # Asumiendo que hay un texto "Libros" en la p\xc3\xa1gina


def test_add_book(client, author):
    response = client.post('/Book/add', data={
        'titleBook': 'new_book',
        'authorId': author.idAuthor
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Libros" in response.data  
    assert b"new_book" in response.data 


def test_edit_book(client, book, author):
    response = client.post(f'/Book/edit/{book.idBook}', data={
        'titleBook': 'updated_book',
        'authorId': author.idAuthor
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"updated_book" in response.data 


def test_delete_book(client, book):
    response = client.get(f'/Book/delete/{book.idBook}', follow_redirects=True)
    assert response.status_code == 200
    assert b"Libros" in response.data  


def test_book_model(app, author):
    book = Book(titleBook="Cien Anos de Soledad", authorId=author.idAuthor)
    db.session.add(book)
    db.session.commit()

    assert book.idBook is not None
    assert book.titleBook == "Cien Anos de Soledad"
    assert book.authorId == author.idAuthor
    assert book.author.nameAuthor == author.nameAuthor
    assert repr(book) == "<Book Cien Anos de Soledad>"
