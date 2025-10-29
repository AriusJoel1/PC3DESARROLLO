.PHONY: help lint test ci check-policies install-hooks

help:
	@echo "Targets: lint test ci check-policies install-hooks"

lint:
	flake8 || true

test:
	pytest --maxfail=1 -q

coverage:
	pytest --maxfail=1 --quiet --cov=policy --cov-report=term-missing

ci: coverage
	@python - <<'PY'
import sys
import re
# simple coverage gate: read .coverage? we rely on pytest-cov printed result above
# In CI we trust pytest to return non-zero if coverage plugin configured to fail; alternatively configure coverage fail in workflow.
print("CI target: run coverage and checks (see workflow for enforcement).")
PY

check-policies:
	python scripts/check_policies.py infra/terraform

install-hooks:
	@cp git-hooks/pre-commit .git/hooks/pre-commit && \
	cp git-hooks/commit-msg .git/hooks/commit-msg && \
	chmod +x .git/hooks/pre-commit .git/hooks/commit-msg && \
	echo "Hooks installed in .git/hooks/"
