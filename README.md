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


## Sprint 2 — Integración IaC (tflint / tfsec) — Instrucciones locales

### Requisitos (local)
- terraform (>=1.0)
- tflint
- tfsec
- python (.venv)

### Instalar dependencia python
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt

### Ejecutar checks
# policy python checks
make check-policies

# run tfsec (produce reports/tfsec-report.json)
make tfsec

# run tflint
make tflint

# parse tfsec in local
python scripts/parse_tfsec.py reports/tfsec-report.json
# exit code 2 = HIGH findings

### Nota
En CI se instalarán tflint/tfsec automáticamente y PRs con HIGH findings serán bloqueados.
