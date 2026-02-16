from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS todos
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT, completed BOOLEAN)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/todos', methods=['GET'])
def get_todos():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT * FROM todos")
    rows = c.fetchall()
    conn.close()
    todos = [{'id': row[0], 'task': row[1], 'completed': bool(row[2])} for row in rows]
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.json
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("INSERT INTO todos (task, completed) VALUES (?, ?)", (data['task'], False))
    conn.commit()
    new_id = c.lastrowid
    conn.close()
    return jsonify({'id': new_id, 'task': data['task'], 'completed': False}), 201

@app.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    data = request.json
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("UPDATE todos SET completed = ? WHERE id = ?", (data['completed'], id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task updated'})

@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("DELETE FROM todos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task deleted'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
