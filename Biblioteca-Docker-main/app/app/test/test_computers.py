from app import db
from app.models.computers import Computer

def test_index(client):
    response = client.get('/computers/')
    assert response.status_code == 200
    assert b"Computadoras" in response.data


def test_add_computer(client):
    response = client.post('/computers/add', data={
        'brandComputer': 'HP',
        'modelComputer': 'ProBook',
        'statusComputer': 'Active'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Computadoras" in response.data
    assert b"ProBook" in response.data


def test_edit_computer(client, computer):
    response = client.post(f'/computers/update/{computer.idComputer}', data={
        'brandComputer': 'Lenovo',
        'modelComputer': 'ThinkPad',
        'statusComputer': 'Active'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"ThinkPad" in response.data


def test_delete_computer(client, computer):
    response = client.post(f'/computers/delete/{computer.idComputer}', follow_redirects=True)
    assert response.status_code == 200
    assert b"Computadoras" in response.data


def test_computer_model(app):
    computer = Computer(brandComputer="Asus", modelComputer="ZenBook", statusComputer="Active")
    db.session.add(computer)
    db.session.commit()

    assert computer.idComputer is not None
    assert computer.brandComputer == "Asus"
    assert computer.modelComputer == "ZenBook"
    assert computer.statusComputer == "Active"
    assert repr(computer) == f'<Computer {computer.idComputer} - Asus ZenBook>'
