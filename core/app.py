from flask import Flask, render_template, redirect, url_for, request, session
from flask_socketio import SocketIO, emit, join_room, leave_room
import uuid
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'  # Секретный ключ для сессий
socketio = SocketIO(app)

# Загрузка белого списка пользователей из CSV
def load_allowed_users():
    allowed_users = {}
    with open('core/list/user.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            allowed_users[row['username']] = row['password']
    return allowed_users

ALLOWED_USERS = load_allowed_users()

# Хранилище для сессий (в памяти)
sessions = {}

# Главная страница с авторизацией
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Проверяем, есть ли пользователь в белом списке
        if username in ALLOWED_USERS and ALLOWED_USERS[username] == password:
            session['username'] = username  # Сохраняем пользователя в сессии
            return redirect(url_for('create_session'))
        else:
            return "Неверный логин или пароль", 401

    return render_template('login.html')

# Страница создания сессии
@app.route('/create_session')
def create_session():
    if 'username' not in session:
        return redirect(url_for('login'))  # Перенаправляем на авторизацию

    # Создаем новую сессию
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "content": "hi there",
        "language": "python",
        "users": 0,
        "creator": session['username']  # Сохраняем создателя сессии
    }
    return redirect(url_for('editor', session_id=session_id))

# Редактор кода
@app.route('/editor/<session_id>')
def editor(session_id):
    if session_id not in sessions:
        return "Сессия не найдена", 404

    # Проверяем, авторизован ли пользователь
    is_creator = session.get('username') == sessions[session_id].get('creator')
    return render_template('editor.html', session_id=session_id, is_creator=is_creator)

# Завершение сессии
@app.route('/end_session/<session_id>')
def end_session(session_id):
    if session_id in sessions:
        if sessions[session_id]['creator'] == session.get('username'):
            del sessions[session_id]  # Удаляем сессию
            return "Сессия завершена", 200
        else:
            return "Только создатель может завершить сессию", 403
    return "Сессия не найдена", 404


@socketio.on('change_language')
def handle_change_language(data):
    session_id = data.get('session_id')
    language = data.get('language')
    if session_id in sessions:
        sessions[session_id]["language"] = language
        emit("language_changed", {"language": language}, room=session_id)


# Реалтайм-синхронизация
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

            # Отправляем текущий язык новому участнику
            emit("language_changed", {
                "language": sessions[session_id]["language"]
            }, room=session_id)

            # Отправляем текущее содержимое редактора
            emit("code", {
                "content": sessions[session_id]["content"],
                "from_server": True
            }, room=session_id)
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
    print(f"Получены изменения для сессии: {session_id}")
    if session_id not in sessions:
        return
    if data.get('type') == 'code':
        sessions[session_id]["content"] = data.get('content')
        emit("code", {"content": data.get('content'), "from_server": True}, room=session_id, include_self=False)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)