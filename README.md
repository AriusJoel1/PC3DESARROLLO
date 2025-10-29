# PC3-Proyecto5-grupo13
# Proyecto 5 — Policy-as-Code (local) — Sprint 1

## Objetivo Sprint 1
- Implementar conjunto mínimo de políticas localmente.
- Crear tests parametrizados para validar reglas.
- Proveer hooks Git iniciales (pre-commit, commit-msg).
- Configurar CI básico que ejecute lint, tests y verifique cobertura ≥85%.

## Estructura
(Ver sección "Estructura de carpetas" en docs)

## Cómo ejecutar localmente
1. Instalar dependencias (recomendado entorno virtual):
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # opcional: pytest, pytest-cov, flake8
