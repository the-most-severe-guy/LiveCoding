const editor = CodeMirror.fromTextArea(document.getElementById('editor'), {
    lineNumbers: true,
    mode: 'python', // По умолчанию Python
    theme: 'dracula', // Темная тема
});

const languageSelect = document.getElementById('language');
const sessionId = document.getElementById('session_id').value;

// Подключаемся к сессии
const socket = io();

// Присоединяемся к сессии
socket.emit('join', { session_id: sessionId });

// Флаг для игнорирования изменений от сервера
let ignoreChanges = false;

// Обработка сообщений от сервера
socket.on('code', (data) => {
    if (data.from_server) {
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
    socket.emit('code', {
        content: content,
        session_id: sessionId,
    });
});

// Обработка выбора языка
languageSelect.addEventListener('change', (event) => {
    const mode = event.target.value;
    editor.setOption('mode', mode);
});

// Копирование ссылки
const copyLinkButton = document.getElementById('copy-link');
copyLinkButton.addEventListener('click', async () => {
    const sessionId = document.getElementById('session_id').value;
    const url = `${window.location.origin}/session/${sessionId}`;

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
    window.location.href = '/'; // Перезагружаем страницу для создания новой сессии
});