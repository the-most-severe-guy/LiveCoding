# LiveCoding

**LiveCoding** is a real-time collaborative code editor with syntax highlighting for multiple programming languages. It's perfect for pair programming, technical interviews, or teaching.

## Features

- **Real-time collaboration**: Share a session link and code together in real-time.
- **Syntax highlighting**: Supports Python, JavaScript, Java, Kotlin, C++, PHP, Ruby, Rust, Swift, Go, and more.
- **No registration required**: Just open the site, and you're ready to go.
- **Dark theme**: Eye-friendly dark mode by default.
- **Session management**: Start a new session with a single click.

## Getting Started

### Prerequisites

- Python 3.7+
- Flask
- Flask-SocketIO

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/the-most-severe-guy/LiveCoding.git
   cd LiveCoding
   ```

2. Install dependencies:
   ```bash
   pip install -r core/requirements.txt
   ```

3. Run the server:
   ```bash
   python core/app.py
   ```

4. Open your browser and navigate to `http://localhost:5000`.

### Docker Support

You can also run the project using Docker:

1. Build the Docker image:
   ```bash
   docker-compose build
   ```

2. Start the container:
   ```bash
   docker-compose up
   ```

3. Open your browser and navigate to `http://localhost:5000`.

## Supported Languages

- Python
- JavaScript
- TypeScript
- HTML
- CSS
- Java
- Kotlin
- C
- C++
- C#
- PHP
- Ruby
- Rust
- Swift
- Go
- Objective-C

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [CodeMirror](https://codemirror.net/) for the awesome code editor.
- [Flask](https://flask.palletsprojects.com/) and [Flask-SocketIO](https://flask-socketio.readthedocs.io/) for the backend.