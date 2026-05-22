#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import subprocess
from pathlib import Path


DEFAULT_JURISDICTIONS = [
    "es",
    "es-an",
    "es-ar",
    "es-as",
    "es-cb",
    "es-cl",
    "es-cm",
    "es-cn",
    "es-ct",
    "es-ex",
    "es-ga",
    "es-ib",
    "es-mc",
    "es-md",
    "es-nc",
    "es-pv",
    "es-ri",
    "es-vc",
]

ALIASES = {
    "es": ["españa", "nacional", "estatal", "boe", "estatal"],
    "es-an": ["andalucía", "andalucia", "junta de andalucía", "boja"],
    "es-ar": ["aragón", "aragon", "gobierno de aragón", "boa"],
    "es-as": ["asturias", "principado de asturias", "bopa"],
    "es-cb": ["cantabria", "boc"],
    "es-cl": ["castilla y león", "castilla y leon", "cyl", "bocyl"],
    "es-cm": ["castilla-la mancha", "castilla la mancha", "clm", "docm"],
    "es-cn": ["canarias"],
    "es-ct": ["cataluña", "catalunya", "generalitat", "dogc"],
    "es-ex": ["extremadura", "doe"],
    "es-ga": ["galicia", "galiza", "xunta", "dog"],
    "es-ib": ["illes balears", "islas baleares", "baleares", "boib"],
    "es-mc": ["murcia", "región de murcia", "region de murcia", "carm", "borm"],
    "es-md": ["madrid", "comunidad de madrid", "cam", "bocm"],
    "es-nc": ["navarra", "comunidad foral de navarra", "gobierno de navarra", "bon"],
    "es-pv": ["país vasco", "pais vasco", "euskadi", "gobierno vasco", "bopv"],
    "es-ri": ["la rioja", "rioja", "bor"],
    "es-vc": ["comunidad valenciana", "comunitat valenciana", "valencia", "generalitat valenciana", "dogv"],
}

STOPWORDS = {
    "a",
    "al",
    "con",
    "de",
    "del",
    "el",
    "en",
    "la",
    "las",
    "lo",
    "los",
    "o",
    "por",
    "que",
    "sobre",
    "un",
    "una",
    "y",
    "busca",
    "buscar",
    "consulta",
    "dime",
    "explícame",
    "explicame",
    "qué",
    "que",
    "cual",
    "cuál",
    "dice",
    "actualmente",
    "recientes",
    "reciente",
    "modificaciones",
    "modificacion",
    "cambió",
    "cambio",
    "cambiar",
    "normativa",
    "leyes",
    "ley",
    "articulo",
    "artículo",
}


def run(cmd: list[str]) -> int:
    return subprocess.call(cmd)


def infer_jurisdictions(query: str) -> list[str]:
    q = query.lower()
    hits: list[str] = []
    for folder, aliases in ALIASES.items():
        if any(alias in q for alias in aliases):
            hits.append(folder)
    ordered = [j for j in DEFAULT_JURISDICTIONS if j in hits]
    return ordered


def extract_article_variants(query: str) -> list[str]:
    match = re.search(r"\bart(?:ículo|\.?)\s*(\d+[a-zA-Z.]*)\b", query, re.IGNORECASE)
    if not match:
        return []
    n = match.group(1)
    variants = [
        f"Artículo {n}",
        f"Art. {n}",
        f"art {n}",
        f"artículo {n}",
        f"###### Artículo {n}",
        f"###### Art. {n}",
    ]
    return variants


def token_variants(query: str) -> list[str]:
    tokens = []
    for raw in re.split(r"[^0-9A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+", query):
        token = raw.strip().lower()
        if len(token) < 4:
            continue
        if token in STOPWORDS:
            continue
        if token not in tokens:
            tokens.append(token)
    return tokens


def main() -> int:
    parser = argparse.ArgumentParser(description="Search Legalize ES repository.")
    parser.add_argument("query", nargs="+", help="Search text or law name")
    parser.add_argument(
        "--repo",
        default=os.environ.get("LEGALIZE_ES_REPO", "."),
        help="Repository path; defaults to LEGALIZE_ES_REPO or current directory",
    )
    parser.add_argument(
        "--jurisdiction",
        action="append",
        default=[],
        help="Prioritize one or more jurisdiction folders such as es or es-vc",
    )
    parser.add_argument("--limit", type=int, default=30, help="Maximum matches per rg call")
    args = parser.parse_args()

    query = " ".join(args.query).strip()
    repo = Path(args.repo)

    search_dirs: list[str] = []
    if args.jurisdiction:
        for item in args.jurisdiction:
            if item not in search_dirs:
                search_dirs.append(item)
    else:
        inferred = infer_jurisdictions(query)
        search_dirs.extend(inferred)

    if "es" not in search_dirs:
        search_dirs.append("es")

    for item in DEFAULT_JURISDICTIONS:
        if item not in search_dirs:
            search_dirs.append(item)

    patterns = [query]
    patterns.extend(extract_article_variants(query))
    patterns.extend(token_variants(query))
    seen = set()
    patterns = [p for p in patterns if not (p in seen or seen.add(p))]

    cmd = [
        "rg",
        "-n",
        "-i",
        "-C",
        "2",
        "-m",
        str(args.limit),
        "--glob",
        "*.md",
    ]
    for pattern in patterns:
        cmd.extend(["-e", pattern])
    cmd.extend([str(repo / d) for d in search_dirs])
    return run(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
