.PHONY: help lint test ci check-policies install-hooks

help:
	@echo "Tareas disponibles: lint, test, ci, check-policies, install-hooks"

lint:
	flake8 || true

test:
	PYTHONPATH=. pytest --maxfail=1 -q

coverage:
	PYTHONPATH=. pytest --maxfail=1 --quiet --cov=policy --cov-report=term-missing

ci:
	PYTHONPATH=. pytest --cov=policy --cov-report=term-missing

check-policies:
	PYTHONPATH=. python scripts/check_policies.py infra/terraform

install-hooks:
	@cp git-hooks/pre-commit .git/hooks/pre-commit && \
	cp git-hooks/commit-msg .git/hooks/commit-msg && \
	chmod +x .git/hooks/pre-commit .git/hooks/commit-msg && \
	echo "Hooks instalados en .git/hooks/"

# Sprint 2

tflint:
	@echo "Ejecutando tflint..."
	@cd infra/terraform && tflint || true

tfsec:
	@echo "Ejecutando tfsec..."
	@cd infra/terraform && tfsec --format json --out ../../reports/tfsec-report.json || true

policy-scan:
	@echo "Ejecutando análisis de políticas..."
	PYTHONPATH=. python scripts/check_policies.py infra/terraform || true
	@echo "Procesando resultados de tfsec..."
	python scripts/parse_tfsec.py reports/tfsec-report.json || (echo "TFSEC encontró hallazgos de severidad ALTA" && exit 2) || true

install-tools:
	@echo "Instalación local de herramientas: terraform / tflint / tfsec (proceso manual)"
	@echo "Consulta el README para los pasos específicos según tu sistema"
