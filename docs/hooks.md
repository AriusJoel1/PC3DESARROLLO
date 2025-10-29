# Hooks Git - Instalación y uso

## Instalación (local)
Desde la raíz del repo:
```bash
mkdir -p .git/hooks
cp git-hooks/pre-commit .git/hooks/pre-commit
cp git-hooks/commit-msg .git/hooks/commit-msg
chmod +x .git/hooks/pre-commit .git/hooks/commit-msg
