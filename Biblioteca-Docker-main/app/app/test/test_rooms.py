from app import db
from app.models.rooms import Room

def test_index(client):
    response = client.get('/room/')
    assert response.status_code == 200
    assert b"Salas" in response.data


def test_add_room(client):
    response = client.post('/room/add', data={
        'name': 'Sala Multimedia',
        'description': 'Sala equipada con proyectores'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Salas" in response.data
    assert b"Sala Multimedia" in response.data


def test_edit_room(client, room):
    response = client.post(f'/room/edit/{room.id}', data={
        'name': 'Sala Actualizada',
        'description': 'Descripcion actualizada'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Sala Actualizada" in response.data


def test_delete_room(client, room):
    response = client.get(f'/room/delete/{room.id}', follow_redirects=True)
    assert response.status_code == 200
    assert b"Salas" in response.data


def test_room_model(app):
    room = Room(name="Sala de Conferencias", description="Espacio para eventos grandes")
    db.session.add(room)
    db.session.commit()

    assert room.id is not None
    assert room.name == "Sala de Conferencias"
    assert room.description == "Espacio para eventos grandes"
    assert repr(room) == f'<Room {room.id} - Sala de Conferencias>'
