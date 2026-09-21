from app import db
from app.models.authors import Author

def test_index(client):
    response = client.get('/Author/')
    assert response.status_code == 200
    assert b"Autores" in response.data  # Asumiendo que hay un texto "Autores" en la p\xc3\xa1gina


def test_add_author(client):
    response = client.post('/Author/add', data={
        'nameAuthor': 'new_author',
        'nationalityAuthor': 'new_nationality'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Autores" in response.data  # Asumiendo que redirige a la lista de autores
    assert b"new_author" in response.data  # Asumiendo que el nombre del autor se muestra en la p\xc3\xa1gina


def test_edit_author(client, author):
    response = client.post(f'/Author/edit/{author.idAuthor}', data={
        'nameAuthor': 'updated_author',
        'nationalityAuthor': 'updated_nationality'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"updated_author" in response.data  # Asumiendo que el nombre del autor actualizado se muestra en la p\xc3\xa1gina


def test_delete_author(client, author):
    response = client.get(f'/Author/delete/{author.idAuthor}', follow_redirects=True)
    assert response.status_code == 200
    assert b"Autores" in response.data  # Asumiendo que hay un mensaje o redirecci\xc3\xb3n a la lista


def test_list_books_author(client, author):
    response = client.get(f'/Author/list/{author.idAuthor}', follow_redirects=True)
    assert response.status_code == 200
    assert b"Lista de Libros" in response.data


def test_author_model(app):
    author = Author(nameAuthor="Gabriel Garcia Marquez", nationalityAuthor="Colombiano")
    db.session.add(author)
    db.session.commit()

    assert author.idAuthor is not None
    assert author.nameAuthor == "Gabriel Garcia Marquez"
    assert author.nationalityAuthor == "Colombiano"
    assert repr(author) == "<Author Gabriel Garcia Marquez>"
