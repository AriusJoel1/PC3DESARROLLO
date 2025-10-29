#!/usr/bin/env python3
"""
scripts/check_policies.py
Uso: python scripts/check_policies.py infra/terraform
Salida: JSON simple con hallazgos por archivo (imprime en stdout)
"""

import sys
import os
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
        print("Usage: check_policies.py <path-to-scan>")
        sys.exit(2)
    base = Path(argv[1])
    if not base.exists():
        print(f"Path {base} not found")
        sys.exit(2)
    fps = discover_files(base)
    if not fps:
        print("No files found to scan.")
        sys.exit(0)
    results = evaluate_files(fps)
    print(json.dumps(results, indent=2))
    # exit with non-zero if any High severity finding: here consider 'secret' or insecure port as high
    high = False
    for fs in results.values():
        for f in fs:
            if f.get("type") in ("secret", "insecure_bind", "common_insecure_port"):
                high = True
    sys.exit(1 if high else 0)

if __name__ == "__main__":
    main(sys.argv)
