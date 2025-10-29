# Documentación de políticas (Sprint 1)

## Objetivo
Conjunto mínimo de políticas para detectar:
- Puertos inseguros (ej: 22 expuesto a 0.0.0.0).
- Secretos en texto plano (aws access keys, passwords).
- Nombres de recursos que incumplen la convención (solo minúsculas y guiones).

## Implementación (Sprint 1)
- Reglas implementadas en `policy/checks.py` como funciones Python.
- Ejemplos Rego en `policy/rules/` para futura integración con OPA/Conftest.
- CLI: `scripts/check_policies.py <path>` -> Escanea archivos `.tf`, `.yml`, `.yaml`, `.json`.

## Severidad
- `High`: secret expuesto, puertos SSH abiertos a 0.0.0.0.
- `Medium`: naming convention violations.
- `Low`: heurísticas menos seguras (no aplicadas todavía).

## Cómo añadir reglas
1. Añadir función en `policy/checks.py`.
2. Añadir tests en `tests/policy/`.
3. Ejecutar `pytest` y ajustar cobertura.
