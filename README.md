# 🧠 Brainfuck MD5 Collision Challenge

<div align="center">

[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen)](https://collision.hacknroll.academy/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.1-lightgrey.svg)](https://flask.palletsprojects.com/)

*A cryptographic challenge combining Brainfuck esoteric programming with MD5 collision exploitation*


[Try the Challenge](https://collision.hacknroll.academy/) • [View Source](https://collision.hacknroll.academy/source) • [Hall Of Fame](HALL_OF_FAME.md) • [Report Bug](https://github.com/maycon/bf-md5-collision/issues)

</div>

---

## 📖 Overview

This challenge is inspired by a classic [g]old challenge from **SmashTheStack**, reimagined with a modern web interface. The goal is to create two different Brainfuck programs that:

1. Produce **different outputs** when executed
2. Have **identical MD5 hashes** (MD5 collision)

### 🎯 Challenge Objectives

- **File 1** must output: `Rock N Roll`
- **File 2** must output: `Hack N Roll`
- Both files must have the **same MD5 hash**

Sounds impossible? That's the beauty of MD5 collision attacks! 🎭

---

## 🚀 Quick Start

### Try Online

Visit [collision.hacknroll.academy](https://collision.hacknroll.academy/) to test your solution without any installation!

### Run Locally with Docker

```bash
# Clone the repository
git clone https://github.com/maycon/bf-md5-collision.git
cd bf-md5-collision

# Start with Docker Compose
docker compose up

# Access the challenge at http://localhost:8000
```

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/maycon/bf-md5-collision.git
cd bf-md5-collision

# Install dependencies with uv (recommended)
uv sync

# Or with pip
pip install -r requirements.txt

# Run the application
python src/main.py
```

---

## 🧩 How It Works

### Brainfuck Interpreter

The challenge uses a custom Brainfuck interpreter that supports:
- 30,000 memory cells (standard)
- 8-bit cell values (0-255 with wraparound)
- All standard Brainfuck commands: `><+-.,[]`

### MD5 Collision Exploitation

MD5 is a cryptographic hash function that's vulnerable to collision attacks. This means it's possible to find two different inputs that produce the same hash output. This challenge leverages that weakness!

### The Twist

You need to craft two Brainfuck programs that:
- Execute correctly (no syntax errors)
- Generate specific, different outputs
- Share the same MD5 hash

**Hint**: Think about how MD5 collision attack techniques (like the Chosen-Prefix Collision) can be applied to Brainfuck bytecode! 🤔

---

## 📂 Project Structure

```
bf-md5-collision/
├── src/
│   ├── main.py              # Flask application and Brainfuck interpreter
│   ├── flag.py              # Flag configuration
│   ├── static/
│   │   └── style.css        # UI styling
│   └── templates/
│       └── upload.html      # Main challenge interface
├── bf/
│   ├── rock.bf              # Example: outputs "Rock N Roll"
│   └── hack.bf              # Example: outputs "Hack N Roll"
├── Dockerfile               # Container configuration
├── compose.yaml             # Docker Compose setup
├── pyproject.toml           # Python dependencies
└── README.md                # This file
```

---

## 🔍 Solution Approach

> **Spoiler Alert**: Skip this section if you want to solve it yourself!

<details>
<summary>Click to reveal solution strategy</summary>

### Understanding MD5 Collisions

Modern MD5 collision techniques allow us to generate two files with:
- A common prefix
- Different collision blocks
- Optional suffixes

### Applying to Brainfuck

1. **Identify collision bytes**: Generate an MD5 collision block
2. **Craft valid Brainfuck**: Ensure collision bytes are valid BF commands or comments
3. **Add suffix logic**: After the collision block, add code that:
   - Detects which version it is
   - Outputs the correct string accordingly

### Tools You Can Use

- **HashClash**: Academic tool for MD5 collisions
- **FastColl**: Faster collision generator
- **UniColl**: Universal collision technique

For a detailed walkthrough, see [SOLUTION.md](./SOLUTION.md)

</details>

---

## 🛠️ Development

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- Docker (optional)

### Setting Up Development Environment

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies in development mode
uv sync --dev

# Run with auto-reload
python src/main.py
```

### Running Tests

```bash
# Run unit tests
pytest

# Run with coverage
pytest --cov=src
```

---

## 🎨 Features

- **Modern UI**: Clean, responsive interface with syntax highlighting
- **Real-time Validation**: Instant feedback on your submissions
- **Source Code View**: Transparent - view the challenge source code
- **Docker Support**: Easy deployment with multi-stage builds
- **Production Ready**: Gunicorn WSGI server with worker configuration

---

## 🏆 Hall of Fame

**Top Solvers** (ranked by smallest total file size):

*Awaiting first submission - be the first!*

[**View Hall of Fame →**](HALL_OF_FAME.md) | [**Submit Your Solution →**](HALL_OF_FAME.md#how-to-submit-your-solution)

Solved the challenge? Add your name to the Hall of Fame by submitting a Pull Request!

---

## 🤝 Contributing

Contributions are welcome! Whether it's:

- 🐛 Bug fixes
- ✨ New features
- 📝 Documentation improvements
- 🎨 UI enhancements

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

---

## 📜 Credits & Attribution

This challenge is based on the **[g]old challenge from SmashTheStack**, a pioneering wargaming platform that inspired countless security enthusiasts.

### Original Challenge
- **Platform**: SmashTheStack
- **Name**: [g]old
- **Concept**: MD5 collision exploitation in a constrained environment

### This Implementation
- **Author**: [Maycon](https://github.com/maycon)
- **Year**: 2024
- **Enhancements**: Modern web interface, Docker deployment, improved UX

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- **Live Demo**: [collision.hacknroll.academy](https://collision.hacknroll.academy/)
- **GitHub**: [maycon/bf-md5-collision](https://github.com/maycon/bf-md5-collision)
- **Report Issues**: [GitHub Issues](https://github.com/maycon/bf-md5-collision/issues)

---

## 🎓 Educational Value

This challenge teaches:
- **Cryptographic Weaknesses**: Understanding MD5 collision attacks
- **Esoteric Programming**: Working with Brainfuck
- **Binary Manipulation**: Crafting specific byte sequences
- **Security Concepts**: Hash function vulnerabilities

Perfect for:
- CTF competitions
- Security training
- Programming challenges
- Educational demonstrations

---

<div align="center">

**Made with ❤️ by the security community**

*Remember: This is for educational purposes only!*

⭐ Star this repo if you found it interesting! ⭐

</div>