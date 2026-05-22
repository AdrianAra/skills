# Patrones de búsqueda

## Objetivo

Find the right law quickly, then verify the current text and history without inventing anything.

## Resolución del repositorio

Before running commands, resolve the repository path in this order:

1. Use `LEGALIZE_ES_REPO` if the environment variable is set.
2. Use a path explicitly provided by the user.
3. Use the current working directory only if it contains `.git` and jurisdiction folders such as `es`, `es-vc`, or `es-cm`.
4. If unresolved, ask the user for the path where `legalize-es` was cloned.

In examples, `<LEGALIZE_ES_REPO>` means the resolved repository path.

## Búsqueda por nombre o materia

- Start with the law title, the known subject, and one or two strong keywords.
- Use `rg` over the relevant jurisdiction folder first.
- If there is no explicit jurisdiction, search `es` first and then expand.

Example:

```bash
rg -n -i --glob '*.md' 'vivienda|urbanismo|constitución' <LEGALIZE_ES_REPO>/es <LEGALIZE_ES_REPO>/es-*
```

## Búsqueda por artículo

- Search these variants together:
 - `Artículo 10`
 - `Art. 10`
 - `art 10`
 - `artículo 10`
- If the user gives only the number, search the article heading and the content around it.

Example:

```bash
rg -n -i --glob '*.md' '###### Artículo 135|###### Art. 135|Artículo 135|Art\. 135|art 135|artículo 135' <LEGALIZE_ES_REPO>/es/BOE-A-1978-31229.md
```

## Búsqueda de texto vigente

1. Find the candidate file.
2. Read the frontmatter.
3. Extract the relevant section from the body.
4. Cite the official identifier and official link when available.
5. Show the local path only if the user asks for technical traceability, debug, commands, or the file path.
6. Say explicitly if the answer is a summary.

Useful commands:

```bash
sed -n '1,80p' FILE
rg -n -i 'palabra clave' FILE
```

## Historia y reformas

- Use `git log --oneline -- <file>` to see the full change history of a specific law.
- Use `git show <commit> -- <file>` to inspect the reform that touched that file.
- Use `git diff <old>..<new> -- <file>` to explain what changed between versions.
- Use `git blame -L start,end -- <file>` only when you need line-level attribution.

Examples:

```bash
git -C <LEGALIZE_ES_REPO> log --oneline -- es/BOE-A-1978-31229.md
git -C <LEGALIZE_ES_REPO> show 2da8d9ec2 -- es/BOE-A-1978-31229.md
git -C <LEGALIZE_ES_REPO> diff 43b53dc31..2da8d9ec2 -- es/BOE-A-1978-31229.md
```

## Búsqueda histórica avanzada

- Para saber cuándo se añadió o eliminó una frase concreta, usar `git log -S "<texto>" -- <file>`.
- Para detectar cambios por patrón o expresión regular, usar `git log -G "<patrón>" --oneline -- <file>`.
- Para obtener el estado histórico de una norma en una fecha concreta, usar:

```bash
git -C <LEGALIZE_ES_REPO> show $(git -C <LEGALIZE_ES_REPO> rev-list -1 --before="YYYY-MM-DD" HEAD):<file>
```

## Safety and accuracy

- Never state that a rule is in force, repealed, or amended until the file and history support it.
- Prefer the repo evidence over memory.
- When the text and the history disagree, trust the Git history for the specific change and the file for the current consolidated text.
