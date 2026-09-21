# save_url

[![PyPI version](https://img.shields.io/pypi/v/save_url.svg)](https://pypi.org/project/save_url/)
[![Python versions](https://img.shields.io/pypi/pyversions/save_url.svg)](https://pypi.org/project/save_url/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

A CLI utility to save any web page into a single, self-contained HTML file with an automatic and structured filename. It uses [single-file-cli](https://github.com/gildas-lormeau/single-file-cli) as its default backend (with optional [monolith](https://github.com/Y2Z/monolith) support).

---

## ✨ Features

- **Self-contained HTML**: Bundles CSS, JavaScript, images, and fonts into a single offline `.html` file.
- **Multiple Backends**:
  - **`singlefile`** *(default)*: High-fidelity capture supporting modern JavaScript/SPAs via `single-file-cli`.
  - **`monolith`**: Ultra-fast, lightweight Rust-based capture without requiring a browser engine.
- **Automatic Title Extraction**: Retrieves the page title using `mechanize` (with automatic fallback to regex search on `<title>` tag or interactive prompt).
- **Structured Filenames**: Names output files predictably by default with timestamp and page title:
  ```text
  YYYYMMDD HHMM Page Title.html
  ```
- **Customizable Output**: Option to omit the date/time prefix (`--notime`).
- **Colorful CLI Feedback**: Displays operation status, error reporting, and humanized saved file sizes.

---

## 📋 Prerequisites

`save_url` requires a backend executable in your system `$PATH`:

### 1. Default Backend: SingleFile CLI (Recommended)

Requires Node.js and a Chromium-based browser (Chromium, Google Chrome, etc.):

```bash
npm install -g single-file-cli
```

### 2. Alternative Backend: Monolith

- **Via Cargo (Rust)**:
  ```bash
  cargo install monolith
  ```
- **Gentoo Linux**:
  Available in [turulomio's portage repository](https://github.com/turulomio/myportage/tree/master/www-apps/monolith).
- **Other Platforms / Prebuilt Binaries**:
  Visit the [monolith releases page](https://github.com/Y2Z/monolith/releases).

---

## 🚀 Installation

### Using pip / pipx

```bash
pip install save_url
```

Or with `pipx` (recommended for CLI tools):

```bash
pipx install save_url
```

### Gentoo Linux

An ebuild is available in the [myportage](https://github.com/turulomio/myportage/tree/master/www-apps/save_url) repository:

```bash
emerge -av www-apps/save_url
```

---

## 📖 Usage

### Basic Usage (SingleFile Backend)

Save a web page with the default timestamp prefix using SingleFile:

```bash
save_url https://www.kde.org
```

**Output example:**
```text
20260921 0752 KDE Community Home - KDE.org.html
```

### Use Monolith Backend

To use the fast `monolith` backend instead:

```bash
save_url https://www.kde.org -b monolith
```

### Omit Date & Time Prefix

To save the file using only the page title:

```bash
save_url https://www.kde.org --notime
```

**Output example:**
```text
KDE Community Home - KDE.org.html
```

### Command-Line Options

```text
usage: save_url [-h] [--version] [-b {singlefile,monolith}] [--notime] url

Script to save an url in a single file with an automatic and structured name.

positional arguments:
  url                   Url to save

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -b, --backend {singlefile,monolith}
                        Backend to use: 'singlefile' (default) or 'monolith'
  --notime              Removes date and time from the beginning of the file name
```

---

## 🛠️ Development & Testing

This project uses [Poetry](https://python-poetry.org/) and [poethepoet](https://github.com/nat-n/poethepoet) for development tasks.

```bash
# Clone the repository
git clone https://github.com/turulomio/save_url.git
cd save_url

# Install dependencies
poetry install

# Run unit tests with coverage
poetry run poe test

# Manage and compile translations
poetry run poe translate
```

---

## 📄 License

This project is licensed under the **GPL-3.0-only** License. See the [LICENSE.txt](LICENSE.txt) file for details.

Developed by **Mariano Muñoz** ([@turulomio](https://github.com/turulomio)).
