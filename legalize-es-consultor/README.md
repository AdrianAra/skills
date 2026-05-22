# legalize-es-consultor

Skill para consultar legislación española estatal y autonómica usando el repositorio [legalize-es](https://github.com/legalize-dev/legalize-es), mantenido por [legalize-dev](https://github.com/legalize-dev).

El repositorio legalize-es modela la legislación española como un repositorio Git: cada ley es un fichero Markdown y cada reforma queda registrada como un commit. Actualmente incluye legislación estatal y autonómica organizada por carpetas como es, es-vc, es-cm, etc.

## Qué permite hacer

Esta skill ayuda a un agente de IA a responder preguntas en lenguaje natural sobre legislación española, por ejemplo:

- consultar el texto vigente de una ley o artículo;
- buscar normas por materia, título, comunidad autónoma o identificador oficial;
- localizar legislación estatal o autonómica;
- analizar reformas históricas usando Git;
- comparar cambios entre versiones;
- citar referencias oficiales como BOE, DOGV, DOCM, BOCM, BOJA, etc.

## Requisitos

Antes de usar la skill, debes clonar el repositorio original legalize-es:
git clone https://github.com/legalize-dev/legalize-es.git ~/repos/legalize-es

Después, define la variable de entorno LEGALIZE_ES_REPO apuntando a la ruta donde hayas clonado el repositorio:
export LEGALIZE_ES_REPO=~/repos/legalize-es

Ejemplo con ruta absoluta:
export LEGALIZE_ES_REPO=/home/usuario/repos/legalize-es

## Estructura esperada del repositorio legalize-es

La skill espera que LEGALIZE_ES_REPO apunte a la raíz del repositorio legalize-es:
legalize-es/
├── es/
├── es-an/
├── es-ar/
├── es-cm/
├── es-vc/
└── ...

La carpeta es contiene legislación estatal. Las carpetas es-* contienen legislación autonómica.

## Ejemplos de uso
¿Qué dice actualmente el artículo 135 de la Constitución Española?
¿Qué reformas ha tenido el artículo 49 de la Constitución?
Busca leyes valencianas sobre vivienda.
¿Qué leyes hay en Castilla-La Mancha relacionadas con urbanismo?
¿Cuándo se modificó por última vez la Ley 8/2004 de Vivienda de la Comunidad Valenciana?
Compara la última versión de la ley valenciana de vivienda con la anterior reforma.

## Citas oficiales

La skill prioriza las referencias oficiales:

1. Si el frontmatter de la norma incluye una URL oficial, la utiliza.
2. Si el identificador es BOE-A-*, construye el enlace oficial al BOE.
3. Si es una norma autonómica y no hay URL oficial, cita el identificador oficial sin inventar enlaces.
4. Si hay URL disponible, la muestra como enlace Markdown sobre el identificador.

Ejemplo:
[BOE-A-1978-31229](https://www.boe.es/buscar/act.php?id=BOE-A-1978-31229)

## Análisis histórico

Para preguntas sobre reformas, modificaciones o versiones anteriores, la skill utiliza comandos Git sobre el repositorio legalize-es, incluyendo:
git log
git diff
git show
git log -S
git log -G

Esto permite consultar cuándo cambió una norma, qué commit introdujo una modificación y qué diferencias existen entre versiones.

## Jurisdicciones soportadas

La skill incluye mapeo de jurisdicciones estatales y autonómicas, por ejemplo:

- es: España, legislación estatal, BOE.
- es-vc: Comunidad Valenciana, Comunitat Valenciana, Valencia.
- es-cm: Castilla-La Mancha, CLM.
- es-ct: Cataluña, Catalunya.
- es-md: Comunidad de Madrid.
- es-an: Andalucía.
- es-ga: Galicia.
- es-pv: País Vasco, Euskadi.

También contempla alias y denominaciones habituales para mejorar la búsqueda desde lenguaje natural.

## Notas

Esta skill no contiene una copia del repositorio legalize-es.

El usuario debe clonarlo por separado y configurar LEGALIZE_ES_REPO.

El mérito del dataset legislativo corresponde al proyecto [legalize-es](https://github.com/legalize-dev/legalize-es) y a sus autores/mantenedores.
