.PHONY: help lint test ci check-policies install-hooks

help:
	@echo "Targets: lint test ci check-policies install-hooks"

lint:
	flake8 || true

test:
	pytest --maxfail=1 -q

coverage:
	pytest --maxfail=1 --quiet --cov=policy --cov-report=term-missing

ci:
	pytest --cov=policy --cov-report=term-missing

check-policies:
	PYTHONPATH=. python scripts/check_policies.py infra/terraform

install-hooks:
	@cp git-hooks/pre-commit .git/hooks/pre-commit && \
	cp git-hooks/commit-msg .git/hooks/commit-msg && \
	chmod +x .git/hooks/pre-commit .git/hooks/commit-msg && \
	echo "Hooks installed in .git/hooks/"

# Makefile additions for Sprint 2

tflint:
	@echo "Running tflint..."
	@cd infra/terraform && tflint || true

tfsec:
	@echo "Running tfsec..."
	@cd infra/terraform && tfsec --format json --out ../../reports/tfsec-report.json || true

policy-scan:
	@echo "Running policy scanner..."
	PYTHONPATH=. python scripts/check_policies.py infra/terraform || true
	@echo "Running tfsec parser..."
	python scripts/parse_tfsec.py reports/tfsec-report.json || (echo "TFSEC found HIGH findings" && exit 2) || true

install-tools:
	@echo "Install local tools: terraform/tflint/tfsec if available (manual step)"
	@echo "See README for platform-specific commands"

