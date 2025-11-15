import json
import sys
from pathlib import Path


def main(report_path):
    p = Path(report_path)
    if not p.exists():
        print(f"No existe el reporte en {report_path}")
        sys.exit(0)

    data = json.loads(p.read_text(encoding="utf-8"))
    # lista de resultados bajo results
    findings = []
    if isinstance(data, dict) and "results" in data:
        findings = data["results"]
    elif isinstance(data, list):
        findings = data
    else:
        print("Estructura JSON de tfsec desconocida")
        sys.exit(1)

    high = [f for f in findings if f.get("severity", "").upper() == "HIGH"]
    medium = [f for f in findings if f.get("severity", "").upper() == "MEDIUM"]
    low = [f for f in findings if f.get("severity", "").upper() == "LOW"]

    print(f"TFSEC resultados: High={len(high)} Medium={len(medium)} Low={len(low)}")
    # opcionalmente imprimir nombres
    if high:
        print("\nHallazgos High (muestra):")
        for f in high[:10]:
            print(
                f"- {f.get('rule_id') or f.get('id')} : {f.get('description') or f.get('message')}"
            )
    # salir con código 2 si hay high, 1 si hay medium, 0 en caso contrario
    if len(high) > 0:
        sys.exit(2)
    elif len(medium) > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    report = sys.argv[1] if len(sys.argv) > 1 else "reports/tfsec-report.json"
    main(report)
