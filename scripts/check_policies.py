import sys
import json
from pathlib import Path
from policy.checks import evaluate_files


def discover_files(base: Path, ext=(".tf", ".yml", ".yaml", ".json")):
    files = []
    for p in base.rglob("*"):
        if p.is_file() and p.suffix in ext:
            files.append(str(p))
    return files


def main(argv):
    if len(argv) < 2:
        print("Uso: check_policies.py <ruta-a-escANear>")
        sys.exit(2)
    base = Path(argv[1])
    if not base.exists():
        print(f"La ruta {base} no existe")
        sys.exit(2)
    fps = discover_files(base)
    if not fps:
        print("No se encontraron archivos para escanear.")
        sys.exit(0)
    results = evaluate_files(fps)
    print(json.dumps(results, indent=2))
    # salir con código distinto de cero si hay algún hallazgo de severidad Alta:
    # se considera 'secret' o puerto inseguro como alta severidad
    high = False
    for fs in results.values():
        for f in fs:
            if f.get("type") in ("secret", "insecure_bind", "common_insecure_port"):
                high = True
    sys.exit(1 if high else 0)


if __name__ == "__main__":
    main(sys.argv)
