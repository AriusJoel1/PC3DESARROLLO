#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
show_structure_with_content.py
Muestra la estructura (sin ocultos) y el contenido de archivos de texto (.py, .tf, .sh, etc.).
"""

from pathlib import Path
import argparse

# extensiones que consideramos código o texto
CODE_EXTS = {".py", ".sh", ".bash", ".tf", ".yml", ".yaml", ".json", ".txt", "makefile"}

def is_hidden(path: Path) -> bool:
    """Devuelve True si el archivo o algún directorio padre empieza con '.'"""
    return any(part.startswith(".") for part in path.parts)

def is_text_file(path: Path) -> bool:
    """Intenta leer una pequeña parte para ver si es texto"""
    try:
        with path.open("rb") as f:
            chunk = f.read(1024)
        if b"\x00" in chunk:
            return False
        return True
    except Exception:
        return False

def print_tree_and_content(root: Path):
    """Imprime estructura y contenido de los archivos"""
    for path in sorted(root.rglob("*")):
        if is_hidden(path):
            continue
        if path.is_dir():
            continue
        suffix = path.suffix.lower()
        if suffix in CODE_EXTS or path.name.lower() in CODE_EXTS:
            print(f"\n{path.relative_to(root)}")
            print("-" * len(str(path.relative_to(root))))
            if is_text_file(path):
                try:
                    content = path.read_text(encoding="utf-8", errors="replace")
                    print(content.strip(), "\n")
                except Exception as e:
                    print(f"<<< ERROR leyendo archivo: {e} >>>\n")
            else:
                print("<<< Archivo no de texto >>>\n")

def main():
    parser = argparse.ArgumentParser(description="Muestra estructura y contenido de archivos de código.")
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Ruta del proyecto (por defecto el actual)."
    )
    args = parser.parse_args()
    root = Path(args.root).resolve()

    if not root.exists():
        print(f"❌ El directorio {root} no existe.")
        return

    print(f"📂 Proyecto: {root}\n")
    print_tree_and_content(root)

if __name__ == "__main__":
    main()
