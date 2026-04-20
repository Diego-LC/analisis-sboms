# 🔐 Ciberseguridad 2026 - Análisis de Seguridad

¡Bienvenido! Este libro detalla la automatización de la evaluación de repositorios mediante **SBOM** (Software Bill of Materials), **CodeQL** y **Grype**.

💡 **Tip:** Presiona **Ctrl + Shift + V** (o **Cmd + Shift + V** en Mac) para leer este documento en modo vista previa.

Si todo ha salido bien entonces en este momento se está realizando la instalación de dependencias, esto puede tardar unos minutos(5-10~), mientras tanto te invito a leer este documento para que comprendas la estructura del libro.

---

## 📋 Índice

- [🚀 Inicio Rápido](#inicio-rápido)
- [📊 Análisis Disponibles](#análisis-disponibles)
- [📁 Estructura del Proyecto](#estructura-del-proyecto)
- [🔧 Configuración](#configuración)
- [❓ Ayuda](#ayuda)

---

## 🚀 Inicio Rápido

### 1. Verificar el Entorno

Abre una terminal y ejecuta:

```bash
# Verificar que todo está instalado
uv run scripts/generate_codeql.py --diagnose
```

Deberías ver ✓ en: CodeQL CLI, Node.js, npm, query packs

### 2. Ejecutar Análisis

Idealmente puedes realizar el proceso a traves de los notebook para la mejor experiencia en `/nbs`, sin embargo, también puedes ejecutar los archivos de forma individual

**Para SBOM (Software Bill of Materials):**

```bash
uv run scripts/generate_sboms.py
```

**Para CodeQL (Análisis Estático - Vulnerabilidades en Código):**

```bash
uv run scripts/generate_codeql.py
```

**Para Grype (Escaneo de Vulnerabilidades en Dependencias):**

```bash
uv run scripts/generate_grype.py
```

### 3. Ver Resultados

Los resultados se guardan en `data/results/`:

- SBOMs: `{repo-name}-sbom.json`
- CodeQL: `{repo-name}-codeql.json`

---

## 📊 Análisis Disponibles

### Notebooks de Análisis

| Nombre                      | Ubicación                          | Descripción                                                 |
| --------------------------- | ---------------------------------- | ----------------------------------------------------------- |
| **Generación de SBOMs**     | `nbs/sbom/generacion_sbom.ipynb`   | Genera Software Bill of Materials usando Syft               |
| **Análisis CodeQL**         | `nbs/vuln/generacion_codeql.ipynb` | Análisis de seguridad estático (vulnerabilidades en código) |
| **Escaneo de Dependencias** | `nbs/vuln/generacion_grype.ipynb`  | Escanea vulnerabilidades en dependencias usando Grype       |

### Scripts

| Script               | Ubicación  | Descripción                                |
| -------------------- | ---------- | ------------------------------------------ |
| `generate_sboms.py`  | `scripts/` | Automatiza generación de SBOMs             |
| `generate_codeql.py` | `scripts/` | Automatiza análisis estático (CodeQL)      |
| `generate_grype.py`  | `scripts/` | Automatiza escaneo de dependencias (Grype) |
| `add_submodules.py`  | `scripts/` | Agrega repositorios como submódulos Git    |

---

## 📁 Estructura del Proyecto

```
ciberseguridad_2026/
├── data/
│   ├── repos/           # Repositorios a analizar
│   ├── results/         # Resultados de análisis (JSON)
│   └── repos.json       # Configuración de repos
├── nbs/                 # Notebooks Jupyter
│   ├── sbom/            # Análisis de SBOMs
│   └── vuln/            # Análisis de vulnerabilidades
│       ├── generacion_codeql.ipynb          # CodeQL
│       ├── explicacion_script_codeql.ipynb
│       ├── generacion_grype.ipynb           # Grype
│       └── explicacion_script_grype.ipynb
├── scripts/             # Automatización
│   ├── generate_sboms.py
│   ├── generate_codeql.py
│   ├── generate_grype.py
│   └── add_submodules.py
├── .devcontainer/       # Configuración DevContainer
└── WELCOME.md           # Este archivo
```

---

## 🔧 Configuración

### Agregar Nuevos Repositorios

1. **Edita `data/repos.json`:**

```json
{
    "repositories": [
        {
            "url": "https://github.com/owner/repo-name.git",
            "path": "data/repos/repo-name",
            "ref": "main"
        }
    ]
}
```

2. **Ejecuta:**

```bash
uv run scripts/add_submodules.py && git submodule update --init --recursive
```

3. **Corre los análisis nuevamente**

### Herramientas Instaladas

- **Python 3.11** con `uv` para gestión de dependencias
- **Syft** para generación de SBOMs
- **CodeQL CLI 2.25.1** para análisis de seguridad
- **Node.js 20** para análisis de JavaScript
- **Git** para control de versiones

---

## ❓ Ayuda

### Problemas Comunes

**❌ La ejecución en el notebook no comienza o carga permanentemente**
El kernel puede mantener bloqueado a vscode, reinicia la ventana con `Ctrl + Shift + P` -> `Developer: reload window` o simplemente cierra y abre vscode.

**Error: "CodeQL CLI not found"**

- Verificar: `codeql version`
- Reconstruir DevContainer: `Dev Containers: Rebuild Container`

**Error: "Query pack cannot be found"**

- Ejecutar: `codeql pack download codeql/python-queries`

**Node.js no disponible (para JavaScript)**

- Reconstruir DevContainer

### Diagnóstico Rápido

```bash
# Diagnosticar CodeQL
uv run scripts/generate_codeql.py --diagnose

# Diagnosticar Grype
uv run scripts/generate_grype.py --diagnose

# Ver versiones instaladas
node --version
npm --version
python --version
```

---

## 📚 Documentación Adicional

- [CodeQL Documentation](https://codeql.github.com/docs/)
- [Syft Documentation](https://github.com/anchore/syft)
- [Software Bill of Materials](https://www.ntia.gov/page/software-bill-materials)

---

**Última actualización**: Abril 2026

¿Necesitas ayuda? Revisa los notebooks en `nbs/` que tienen instrucciones paso a paso.
