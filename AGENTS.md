# Guía para Agentes (AGENTS.md)

Este documento define los estándares, arquitectura, flujo de trabajo y reglas para agentes de IA y desarrolladores que trabajen en el proyecto **`save_url`**.

---

## 📌 Descripción del Proyecto

`save_url` es una herramienta de línea de comandos en Python que permite guardar una página web completa en un único archivo HTML autocontenido con un nombre estructurado y fechado automáticamente (`YYYYMMDD HHMM <Título>.html`).

---

## 🛠️ Stack Tecnológico

- **Lenguaje:** Python (>= 3.14, < 4.0.0)
- **Gestor de Paquetes y Entorno:** [Poetry](https://python-poetry.org/)
- **Ejecutor de Tareas:** [PoeThePoet](https://github.com/nat-n/poethepoet)
- **Pruebas y Cobertura:** `pytest` y `pytest-cov`
- **Dependencias Principales:**
  - `pydicts`: Funciones de color (`pydicts.colors`) y formateo de fechas (`pydicts.casts`).
  - `mechanize`: Extracción de títulos de páginas web.
  - `colorama`: Inicialización y estilos de terminal.
- **Backends de Guardado Externos:**
  - `single-file-cli` (**Por defecto**): Renderizado completo con soporte de JavaScript moderno / SPAs.
  - `monolith` (**Opcional**): Renderizado ultraligero y rápido en Rust sin motor de navegador.

---

## 📂 Estructura del Repositorio

```text
save_url/
├── .github/
│   └── workflows/
│       └── ci.yml              # Flujo de CI para GitHub Actions (test + coverage)
├── save_url/
│   ├── __init__.py             # Versión y fecha de versión
│   ├── core.py                 # Lógica principal, CLI y ejecución de backends
│   ├── poethepoet.py           # Tareas de Poe (release, translate, monolith_ebuild)
│   └── locale/                 # Catálogos gettext (es, fr, ru, hi, ro)
├── tests/
│   └── test_save_url.py        # Suite de pruebas unitarias
├── pyproject.toml              # Configuración del proyecto, dependencias y scripts
├── README.md                   # Documentación de cara al usuario
└── AGENTS.md                   # Estándares e instrucciones para agentes
```

---

## 📜 Reglas y Convenciones para Agentes

### 1. 🌐 Gestión de Traducciones (i18n)
- **NO ejecutar ni regenerar traducciones en cada commit:** Las traducciones (`poe translate`) **NO** deben ejecutarse durante commits ordinarios de desarrollo.
- Las traducciones solo se extraen y compilan cuando se prepara una nueva versión (**Release**).
- El soporte multiidioma usa `gettext` con catálogos en `save_url/locale/` para los idiomas: `es`, `fr`, `ru`, `hi`, `ro`.

### 2. 🎨 Uso de Bibliotecas y Estilo de Código
- Para colores y formateo en consola, importar siempre mediante:
  ```python
  from pydicts import colors, casts
  ```
- Usar `casts.dtnaive2str(datetime.now(), "%Y%m%d %H%M")` para el formateo de fecha y hora en nombres de fichero.
- Manejar salidas de error con código de retorno `exit(2)` cuando falte un ejecutable en el sistema.

### 3. 🧪 Pruebas Unitarias y Cobertura
- Cualquier nueva funcionalidad o modificación debe incluir pruebas unitarias en `tests/`.
- Mantener una cobertura de código elevada (mínimo > 90%).
- Ejecutar pruebas con:
  ```bash
  poetry run poe test
  # o directamente:
  poetry run pytest
  ```

---

## 🚀 Comandos Principales de Desarrollo

```bash
# Instalar dependencias
poetry install

# Ejecutar suite de pruebas con reporte de cobertura
poetry run poe test

# Probar la CLI localmente
poetry run save_url --help
poetry run save_url https://www.kde.org --notime

# Tareas de release (solo al preparar versión)
poetry run poe release
poetry run poe translate
```
