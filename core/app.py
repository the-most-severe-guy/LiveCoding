from flask import Flask, render_template, redirect, url_for, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Хранилище для сессий (в памяти)
sessions = {}

@app.route('/')
def index():
    # Создаем новую сессию и перенаправляем пользователя
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "content": "",
        "language": "python",
        "users": 0  # Количество подключенных пользователей
    }
    return redirect(url_for('session', session_id=session_id))

@app.route('/session/<session_id>')
def session(session_id):
    if session_id not in sessions:
        return "Сессия не найдена", 404
    return render_template('index.html', session_id=session_id)

@socketio.on('connect')
def handle_connect():
    print("Клиент подключен")

@socketio.on('disconnect')
def handle_disconnect():
    print("Клиент отключен")

@socketio.on('join')
def handle_join(data):
    session_id = data.get('session_id')
    if session_id in sessions:
        if sessions[session_id]["users"] >= 4:
            emit("error", {"message": "Сессия переполнена (максимум 4 участника)"})
        else:
            join_room(session_id)
            sessions[session_id]["users"] += 1
            # Отправляем текущее содержимое сессии новому участнику
            emit("code", {"content": sessions[session_id]["content"], "from_server": True}, room=session_id)
    else:
        emit("error", {"message": "Сессия не найдена"})

@socketio.on('leave')
def handle_leave(data):
    session_id = data.get('session_id')
    if session_id in sessions:
        leave_room(session_id)
        sessions[session_id]["users"] -= 1

@socketio.on('code')
def handle_code(data):
    session_id = data.get('session_id')
    if session_id not in sessions:
        return
    # Обновляем содержимое сессии
    sessions[session_id]["content"] = data.get('content')
    # Рассылаем изменения всем участникам сессии, кроме отправителя
    emit("code", {"content": data.get('content'), "from_server": True}, room=session_id, include_self=False)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')