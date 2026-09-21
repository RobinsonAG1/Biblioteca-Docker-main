from datetime import datetime, timedelta
from app import db
from app.models.cloans import ComputerLoan

def test_index(client):
    response = client.get('/cloans/')
    assert response.status_code == 200
    assert "Pr\xc3\xa9stamos".encode('utf-8') in response.data or b"Prestamos" in response.data


def test_add_cloan(client, computer, user):
    response = client.post('/cloans/add', data={
        'computerId': computer.idComputer,
        'userId': user.idUser,
        'status': 'Active'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "Pr\xc3\xa9stamos".encode('utf-8') in response.data or b"Prestamos" in response.data


def test_edit_cloan(client, cloan, computer, user):
    response = client.post(f'/cloans/update/{cloan.idLoan}', data={
        'computerId': computer.idComputer,
        'userId': user.idUser,
        'loanDate': '2026-09-21 10:00:00',
        'returnDate': '2026-09-22 10:00:00',
        'status': 'Active'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "Pr\xc3\xa9stamos".encode('utf-8') in response.data or b"Prestamos" in response.data


def test_delete_cloan(client, cloan):
    response = client.post(f'/cloans/delete/{cloan.idLoan}', follow_redirects=True)
    assert response.status_code == 200
    assert "Pr\xc3\xa9stamos".encode('utf-8') in response.data or b"Prestamos" in response.data


def test_return_computer(client, cloan):
    response = client.post(f'/cloans/return/{cloan.idLoan}', follow_redirects=True)
    assert response.status_code == 200
    assert "Pr\xc3\xa9stamos".encode('utf-8') in response.data or b"Prestamos" in response.data


def test_cloan_model(app, computer, user):
    cloan = ComputerLoan(
        computerId=computer.idComputer,
        userId=user.idUser,
        loanDate=datetime.utcnow(),
        returnDate=datetime.utcnow() + timedelta(days=1),
        status="Active"
    )
    db.session.add(cloan)
    db.session.commit()

    assert cloan.idLoan is not None
    assert cloan.computerId == computer.idComputer
    assert cloan.userId == user.idUser
    assert cloan.computer.brandComputer == computer.brandComputer
    assert cloan.user.nameUser == user.nameUser
    assert repr(cloan) == f'<ComputerLoan {cloan.idLoan} of Computer {cloan.computerId} to User {cloan.userId}>'
