# Análisis de Seguridad y SBOMs - Organización Encode

Este repositorio contiene los resultados del análisis sistemático de dependencias y vulnerabilidades (SBOMs) para la organización open-source **[Encode](https://github.com/encode)**. 

El proyecto fue generado en el marco de la actividad de minería de repositorios (`ciberseguridad_2026`) y contiene todas las herramientas necesarias para la extracción, análisis estático y generación de inventarios de software de los repositorios seleccionados.

## 📁 Estructura del Proyecto

* **`analisis_sboms.ipynb`**: Notebook de Jupyter con el análisis cuantitativo final y la interpretación de datos extraídos.
* **`ciberseguridad_2026/`**: Contiene la lógica, los scripts y el entorno para la recolección de los datos.
  * **`data/repos.json`**: Lista de repositorios activos de `encode` configurados para el análisis.
  * **`data/results/`**: Almacena todos los resultados crudos generados (JSON y SARIF) tras ejecutar Syft, Grype y CodeQL.
  * **`scripts/`**: Scripts en Python para ejecutar los procesos de clonación y análisis automatizado.
  * **`.devcontainer/`**: Archivos de configuración para ejecutar este repositorio limpiamente dentro de un contenedor en VS Code.

## 🚀 Cómo reproducir el análisis

Para reproducir los resultados de este repositorio de manera aislada y sin instalar dependencias globales, se recomienda utilizar **VS Code con la extensión de Dev Containers**.

### 1. Preparar el Entorno
Abre la carpeta `ciberseguridad_2026/` en Visual Studio Code. VS Code te sugerirá reabrir la carpeta dentro de un Dev Container. Hazlo para que Docker descargue y prepare el entorno con `syft`, `grype` y `codeql`.

### 2. Ejecutar la recolección
Dentro de la terminal del Dev Container, ejecuta los siguientes comandos en orden:

```bash
# 1. Clonar repositorios de la organización encode
uv run scripts/add_submodules.py
git submodule update --init --recursive

# 2. Generar inventario de dependencias (SBOMs)
uv run scripts/generate_sboms.py

# 3. Analizar vulnerabilidades en dependencias descubiertas
uv run scripts/generate_grype.py

# 4. Escanear vulnerabilidades de código fuente
uv run scripts/generate_codeql.py
```

### 3. Visualización y Análisis Cuantitativo
Una vez finalizados los scripts, la carpeta `data/results/` estará poblada. Dirígete a la raíz de este proyecto y abre el notebook **`analisis_sboms.ipynb`** para revisar las métricas, distribuciones de severidad y el análisis estadístico de la seguridad del proyecto.
