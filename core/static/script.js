const editor = CodeMirror.fromTextArea(document.getElementById('editor'), {
    lineNumbers: true,
    mode: 'python', // По умолчанию Python
    theme: 'dracula', // Тёмная тема
});

const languageSelect = document.getElementById('language');
const sessionId = document.getElementById('session_id').value;

// Подключаемся к сессии
const socket = io();

// Проверка подключения
socket.on('connect', () => {
    console.log('Подключен к серверу');
});

// Проверка ошибок подключения
socket.on('connect_error', (error) => {
    console.error('Ошибка подключения:', error);
});

// Присоединяемся к сессии
socket.emit('join', { session_id: sessionId });

// Обработка сообщений от сервера
socket.on('code', (data) => {
    if (data.from_server) {
        console.log("Получены изменения от сервера:", data.content);
        ignoreChanges = true; // Игнорируем изменения от сервера
        editor.setValue(data.content);
        ignoreChanges = false; // Возвращаем флаг в исходное состояние
    }
});

// Обработка ошибок
socket.on('error', (data) => {
    alert(data.message); // Показываем сообщение об ошибке
});

// Отправляем изменения на сервер
editor.on('change', (instance) => {
    if (ignoreChanges) return; // Игнорируем изменения от сервера
    const content = instance.getValue();
    console.log("Отправка изменений на сервер:", content);
    socket.emit('code', {
        type: 'code',
        content: content,
        session_id: sessionId,
    });
});

// Обработка выбора языка
languageSelect.addEventListener('change', (event) => {
    const mode = event.target.value;
    editor.setOption('mode', mode);

    // Отправляем выбранный язык на сервер
    socket.emit('change_language', {
        session_id: sessionId,
        language: mode,
    });
});

// Обработка изменения языка от сервера
socket.on('language_changed', (data) => {
    const mode = data.language;
    console.log("Получен новый язык:", mode);
    editor.setOption('mode', mode);
    languageSelect.value = mode; // Обновляем выпадающий список
});

// Копирование ссылки
const copyLinkButton = document.getElementById('copy-link');
copyLinkButton.addEventListener('click', async () => {
    const sessionId = document.getElementById('session_id').value;
    const url = `${window.location.origin}/editor/${sessionId}`;

    try {
        // Проверяем, поддерживает ли браузер Clipboard API
        if (!navigator.clipboard) {
            throw new Error("Clipboard API не поддерживается");
        }

        // Копируем ссылку в буфер обмена
        await navigator.clipboard.writeText(url);

        // Показываем уведомление
        alert('Ссылка скопирована!');
    } catch (error) {
        console.error("Ошибка при копировании ссылки:", error);

        // Альтернативный способ для старых браузеров
        const tempInput = document.createElement('input');
        tempInput.value = url;
        document.body.appendChild(tempInput);
        tempInput.select();
        document.execCommand('copy');
        document.body.removeChild(tempInput);

        alert('Ссылка скопирована!');
    }
});

// Новая сессия
const newSessionButton = document.getElementById('new-session');
newSessionButton.addEventListener('click', () => {
    window.location.href = '/create_session';
});

// Завершение сессии
const endSessionButton = document.getElementById('end-session');
endSessionButton.addEventListener('click', () => {
    const sessionId = document.getElementById('session_id').value;
    fetch(`/end_session/${sessionId}`, {
        method: 'GET',
    })
    .then(response => {
        if (response.ok) {
            alert('Сессия завершена');
            window.location.href = '/';  // Перенаправляем на главную страницу
        } else {
            alert('Ошибка при завершении сессии');
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
});