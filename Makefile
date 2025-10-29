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
