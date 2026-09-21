# save_url

[![PyPI version](https://img.shields.io/pypi/v/save_url.svg)](https://pypi.org/project/save_url/)
[![Python versions](https://img.shields.io/pypi/pyversions/save_url.svg)](https://pypi.org/project/save_url/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

A CLI utility to save any web page into a single, self-contained HTML file with an automatic and structured filename. It uses [monolith](https://github.com/Y2Z/monolith) as its backend.

---

## ✨ Features

- **Self-contained HTML**: Bundles CSS, JavaScript, images, and fonts into a single offline `.html` file.
- **Automatic Title Extraction**: Retrieves the page title using `mechanize` (with automatic fallback to regex search on `<title>` tag or interactive prompt).
- **Structured Filenames**: Names output files predictably by default with timestamp and page title:
  ```text
  YYYYMMDD HHMM Page Title.html
  ```
- **Customizable Output**: Option to omit the date/time prefix (`--notime`).
- **Colorful CLI Feedback**: Displays operation status, error reporting, and humanized saved file sizes.

---

## 📋 Prerequisites

`save_url` requires **[monolith](https://github.com/Y2Z/monolith)** to be installed and available in your system `$PATH`.

### Installing Monolith

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

### Basic Usage

Save a web page with the default timestamp prefix:

```bash
save_url https://www.kde.org
```

**Output example:**
```text
20260921 0752 KDE Community Home - KDE.org.html
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
usage: save_url [-h] [--version] [--notime] url

Script to save an url in a single file with an automatic and structured name. It uses monolith as its backend.

positional arguments:
  url         Url to save

options:
  -h, --help  show this help message and exit
  --version   show program's version number and exit
  --notime    Removes date and time from the beginning of the file name
```

---

## 🛠️ Development

This project uses [Poetry](https://python-poetry.org/) and [poethepoet](https://github.com/nat-n/poethepoet) for development tasks.

```bash
# Clone the repository
git clone https://github.com/turulomio/save_url.git
cd save_url

# Install dependencies
poetry install

# Manage translations
poetry run poe translate
```

---

