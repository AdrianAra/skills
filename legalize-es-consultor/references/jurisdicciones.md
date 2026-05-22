# Jurisdicciones

Mapa de carpetas esperado en un clon local del repositorio `legalize-dev/legalize-es`.

## Mapeo de carpetas

- `es`: España, nacional, estatal, BOE, legislación española estatal.
- `es-an`: Andalucía, Junta de Andalucía, BOJA.
- `es-ar`: Aragón, Gobierno de Aragón, BOA.
- `es-as`: Asturias, Principado de Asturias, BOPA.
- `es-cb`: Cantabria, Gobierno de Cantabria, BOC.
- `es-cl`: Castilla y León, CyL, JCYL, BOCYL.
- `es-cm`: Castilla-La Mancha, Castilla la Mancha, CLM, DOCM.
- `es-cn`: Canarias, Gobierno de Canarias, BOC.
- `es-ct`: Cataluña, Catalunya, Generalitat, DOGC.
- `es-ex`: Extremadura, Junta de Extremadura, DOE.
- `es-ga`: Galicia, Galiza, Xunta, DOG.
- `es-ib`: Illes Balears, Islas Baleares, Baleares, BOIB.
- `es-mc`: Murcia, Región de Murcia, CARM, BORM.
- `es-md`: Madrid, Comunidad de Madrid, CAM, BOCM.
- `es-nc`: Navarra, Comunidad Foral de Navarra, Gobierno de Navarra, BON.
- `es-pv`: País Vasco, Euskadi, Gobierno Vasco, BOPV.
- `es-ri`: La Rioja, Gobierno de La Rioja, BOR.
- `es-vc`: Comunidad Valenciana, Comunitat Valenciana, Valencia, Generalitat Valenciana, DOGV.

## Notes

- The repository uses `es-vc`, not `es-cv`.
- When the user says "Valencia" and the context could mean the autonomous community, search `es-vc` first and say that you interpreted it that way.
- If the user does not specify a jurisdiction, search `es` first and then broaden to all `es-*` folders.
