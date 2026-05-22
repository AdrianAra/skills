---
name: legalize-es-consultor
description: "Consultar legislación española estatal y autonómica en un clon local del repositorio Legalize ES. Usar cuando el usuario pregunte por leyes, artículos, reformas, modificaciones, vigencia, histórico Git, comunidades autónomas, BOE, DOGV, DOCM u otra normativa española en lenguaje natural."
---

# Legalize ES Consultor

Use this skill when the user asks about Spanish state or autonomous legislation stored in a local clone of `legalize-dev/legalize-es`.

Before resolving jurisdiction-sensitive queries, read `references/jurisdicciones.md`.
For search, article, history, or diff strategy, read `references/patrones-busqueda.md`.

## Repository location

Resolve the Legalize ES repository path before running searches or Git commands:

1. If the environment variable `LEGALIZE_ES_REPO` exists, use it.
2. If the user explicitly provides a repository path in the conversation, use that path.
3. If neither is available, try the current working directory when it contains `.git` and folders such as `es`, `es-vc`, or `es-cm`.
4. If the repository cannot be resolved, ask the user where they cloned `legalize-es` before running commands.

Use `<LEGALIZE_ES_REPO>` in examples to represent the resolved path. Do not hard-code a local path in public-facing instructions.

## What it does

- Finds the current text of a law, article, disposition, or legal term.
- Locates candidate files by name, subject, or jurisdiction.
- Explains historical changes using Git commits and diffs.
- Prioritizes the correct jurisdiction from natural language.

## Core workflow

1. Detect jurisdiction from the user wording.
2. If the jurisdiction is explicit, search that folder first.
3. If no jurisdiction is explicit, search `es` first, then all autonomous folders.
4. Locate candidate file(s) with `rg` or `scripts/legalize_search.py`.
5. Inspect the file frontmatter and the relevant fragment.
6. For historical questions, run `git log --oneline -- <file>` and then `git show` or `git diff` on the relevant commit(s).
7. Answer with the file path, commit hash, and command evidence when history matters.

## Jurisdiction rules

- `es` means Spain, state, national, BOE, or estatal.
- If the user mentions a community autonomously, prioritize its folder.
- If the question mentions Valencia or Comunitat Valenciana, interpret it as `es-vc` and say so if the wording could be ambiguous.
- If the question is ambiguous and no jurisdiction is stated, start with `es` and then expand to all `es-*` folders.

## Search rules

- Search article variants such as `Artículo 10`, `Art. 10`, `art 10`, and `artículo 10`.
- Search by law name, subject, and legal term together when possible.
- Use frontmatter to confirm `title`, `identifier`, `last_updated`, `status`, `scope`, and `jurisdiction` when present.
- Never claim that a norm is vigente, derogada, or modified without checking the file content and, when relevant, the Git history.

## Output rules

- In normal answers, cite the official norm reference and, when possible, the official link.
- If the frontmatter has an official URL field or equivalent (`source`, `url`, `official_url`, or similar), use that URL.
- Detect official identifiers case-insensitively for citation routing and link construction, but keep the identifier shown to the user exactly as it appears in the frontmatter or file.
- If there is no explicit official URL and the identifier is `BOE-A-*` or `boe-a-*`, build the official BOE link as `https://www.boe.es/buscar/act.php?id=<IDENTIFIER>`.
- If the norm is autonómica (`DOGV-*`, `DOCM-*`, `BOCM-*`, `BOJA-*`, and similar, in any letter case) and there is no official URL in the frontmatter, cite only the official identifier without inventing a link.
- When a URL is available, show it as a Markdown link on the identifier: `[IDENTIFIER](URL)`.
- Do not show bare URLs unless the user explicitly asks for them.
- Keep commit hash and date when you explain a reform or historical change.
- Show the resolved local repository path only if the user explicitly asks for the file, the path, executed commands, technical audit, or debug details.
- Quote or cite the commit hash when you explain a reform.
- If you summarize a fragment, say that it is a summary.

## Tools

- `scripts/legalize_search.py`
- `scripts/legalize_history.py`
- `scripts/legalize_diff.py`
