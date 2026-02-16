import pytest
from app import app, init_db
import json
import os

@pytest.fixture
def client():
    app.config['TESTING'] = True
    # Use a temporary database for testing
    if os.path.exists('test_todo.db'):
        os.remove('test_todo.db')
        
    # Patch SQLite connection in app.py to use test database
    # Assuming app.py connects to 'todo.db', we need to intercept that or make it configurable.
    # For simplicity, let's modify app.py to accept a db configuration, or just mock the db connection.
    # However, since I can't easily refactor app.py without risk, I'll rely on the fact that app.py uses 'todo.db'.
    # A better approach for the test is to rename the real db temporarily or use a specific test config if the app supported it.
    
    # Actually, let's just make the test simple and integration-like.
    # But to avoid messing with the real DB, I should probably refactor app.py slightly to allow DB path configuration.
    # Let's check app.py content again.

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

    # Cleanup is hard if file path is hardcoded. 
    # Let's proceed with a simpler test that mocks sqlite3 or just tests the endpoints assuming a clean state if possible.
    # But `todo.db` is hardcoded.
    
# Let's do a meaningful test by first refactoring app.py slightly to allow overriding the DB name, 
# OR just mock sqlite3.connect. 
# Mocking is safer to avoid touching the real DB.

from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_db_cursor():
    with patch('sqlite3.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        yield mock_cursor

def test_get_todos_empty(client, mock_db_cursor):
    mock_db_cursor.fetchall.return_value = []
    response = client.get('/todos')
    assert response.status_code == 200
    assert response.json == []

def test_add_todo(client, mock_db_cursor):
    mock_db_cursor.lastrowid = 1
    response = client.post('/todos', json={'task': 'Test Task'})
    assert response.status_code == 201
    assert response.json['task'] == 'Test Task'
    assert response.json['id'] == 1
    assert response.json['completed'] == False

def test_update_todo(client, mock_db_cursor):
    response = client.put('/todos/1', json={'completed': True})
    assert response.status_code == 200
    assert response.json['message'] == 'Task updated'

def test_delete_todo(client, mock_db_cursor):
    response = client.delete('/todos/1')
    assert response.status_code == 200
    assert response.json['message'] == 'Task deleted'
