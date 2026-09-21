from datetime import datetime, timedelta
from app import db
from app.models.loans import Loan

def test_index(client):
    response = client.get('/Loan/')
    assert response.status_code == 200
    assert "Pr\xc3\xa9stamos".encode('utf-8') in response.data or b"Prestamos" in response.data


def test_add_loan(client, book, user):
    response = client.post('/Loan/add', data={
        'bookId': book.idBook,
        'userId': user.idUser
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "Pr\xc3\xa9stamos".encode('utf-8') in response.data or b"Prestamos" in response.data


def test_edit_loan(client, loan):
    response = client.post(f'/Loan/edit/{loan.idLoan}', data={
        'returnDate': '2026-10-01',
        'fine': '5.0',
        'status': 'Active'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"5.0" in response.data


def test_delete_loan(client, loan):
    response = client.get(f'/Loan/delete/{loan.idLoan}', follow_redirects=True)
    assert response.status_code == 200
    assert "Pr\xc3\xa9stamos".encode('utf-8') in response.data or b"Prestamos" in response.data


def test_return_book(client, loan):
    response = client.get(f'/Loan/return/{loan.idLoan}', follow_redirects=True)
    assert response.status_code == 200
    assert "Pr\xc3\xa9stamos".encode('utf-8') in response.data or b"Prestamos" in response.data


def test_loan_model(app, book, user):
    loan = Loan(
        bookId=book.idBook,
        userId=user.idUser,
        loanDate=datetime.utcnow(),
        returnDate=datetime.utcnow() + timedelta(days=7),
        fine=0.0,
        status="Active"
    )
    db.session.add(loan)
    db.session.commit()

    assert loan.idLoan is not None
    assert loan.bookId == book.idBook
    assert loan.userId == user.idUser
    assert loan.book.titleBook == book.titleBook
    assert loan.user.nameUser == user.nameUser
    assert repr(loan) == f'<Loan {loan.idLoan} of Book {loan.bookId} to User {loan.userId}>'
