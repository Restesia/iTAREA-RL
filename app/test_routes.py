import sys

import pytest

from app import app


@pytest.fixture
def client():
    """Crea un cliente de prueba para la aplicación Flask."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_inicio(client):
    """Prueba la página de inicio."""
    response = client.get('/')
    assert response.status_code == 200
    assert 'Bienvenido a mi aplicación' in response.data

def test_ruta_invalida(client):
    """Prueba una ruta no válida."""
    response = client.get('/ruta_invalida')
    assert response.status_code == 404
