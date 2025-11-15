import re
from typing import List, Dict


def find_insecure_ports(text: str) -> List[Dict]:
    """
    Busca patrones de puertos inseguros en texto (ej: '0.0.0.0:22' o '22' en provider o resource).
    Retorna lista de dicts con hallazgos.
    """
    findings = []
    # patrón simple: 0.0.0.0:<port> o host = "0.0.0.0" + port
    for match in re.finditer(r"0\.0\.0\.0\s*:\s*(\d{1,5})", text):
        port = int(match.group(1))
        findings.append({"type": "insecure_bind", "port": port, "span": match.span()})

    # patrón HCL típico: "22" en parametro que contenga "port" o "ingress"
    for match in re.finditer(r'(port|ingress)[\s=:\[]+["\']?(\d{1,5})["\']?', text, flags=re.IGNORECASE):
        port = int(match.group(2))
        if port in (22,):  # considered insecure for the policy
            findings.append({"type": "common_insecure_port", "port": port, "span": match.span()})

    return findings


SECRET_REGEXES = [
    re.compile(r"(?i)aws[_-]?access[_-]?key[_-]?id\s*=\s*['\"]?([A-Z0-9]{16,})['\"]?"),
    re.compile(r"(?i)aws[_-]?secret[_-]?access[_-]?key\s*=\s*['\"]?([A-Za-z0-9/+=]{20,})['\"]?"),
    # match password="SuperSecret123!" or similar (any non-empty string with symbols)
    re.compile(r"(?i)password\s*=\s*['\"]([^'\"]{4,})['\"]"),
    re.compile(r"(?i)secret\s*=\s*['\"]([^'\"]{4,})['\"]"),
    re.compile(r"(?i)token\s*=\s*['\"]([^'\"]{4,})['\"]"),
]


def find_secrets(text: str) -> List[Dict]:
    findings = []
    for rx in SECRET_REGEXES:
        for m in rx.finditer(text):
            findings.append({"type": "secret", "match": m.group(0), "span": m.span()})
    return findings


def check_naming_convention(text: str, allowed_pattern: str = r"^[a-z0-9\-]+$") -> List[Dict]:
    """
    Busca nombres de recursos (heurística) y valida pattern simple: lowercase, digits and hyphens.
    Retorna lista de violaciones.
    """
    findings = []
    # heurística: resource "<type>" "<name>" { ... }
    for m in re.finditer(r'resource\s+"[^"]+"\s+"([^"]+)"', text):
        name = m.group(1)
        if not re.match(allowed_pattern, name):
            findings.append({"type": "naming", "name": name, "reason": "invalid chars"})

    return findings


def run_all_checks_on_text(content: str):
    findings = []

    # Detectar 0.0.0.0/0 (insecure bind)
    if re.search(r"(0\.0\.0\.0/0)", content):
        findings.append({"type": "insecure_bind"})

    # Detectar contraseñas o secretos duros dentro de variables
    # Ejemplo: variable "db_password" { default = "SuperSecret123!" }
    secret_pattern = re.compile(
        r'(?i)(password|secret|token)[^=]*=\s*["\']([^"\']+)["\']'
    )
    if secret_pattern.search(content):
        findings.append({"type": "secret"})

    return findings


def evaluate_files(filepaths: List[str]) -> Dict[str, List[Dict]]:
    """
    Dado un listado de archivos, ejecuta checks sobre cada uno y retorna dict filepath -> findings.
    """
    results = {}
    for p in filepaths:
        try:
            with open(p, "r", encoding="utf-8") as fh:
                content = fh.read()
        except Exception as e:
            results[p] = [{"type": "error", "message": f"Could not read file: {e}"}]
            continue
        results[p] = run_all_checks_on_text(content)
    return results
