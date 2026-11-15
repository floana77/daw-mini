# Impacto · FEAT-001 · Prioridad automática de tickets

## Archivos afectados
- `src/tickettriage/tickets.py` · `Ticket` suma los campos `prioridad` y `motivo_prioridad`; `crear_ticket` calcula la prioridad al crear (y quizás recibe un dato VIP, según CLARIFY).
- `src/tickettriage/prioridad.py` (nuevo) · reglas puras y deterministas: palabras clave por nivel, ajuste VIP y armado del motivo.
- `tests/test_prioridad.py` (nuevo) · tests de las reglas (AC-01 a AC-09).
- `tests/test_tickets.py` · sin cambios esperados; los tests actuales tienen que seguir en verde.

## Riesgos
- **Compatibilidad:** si `crear_ticket` suma un parámetro obligatorio (ej. `vip`), se rompen los llamadores actuales. Mitigación: que sea opcional, con default `False`.
- **Falsos positivos o negativos por palabras clave:** "no funciona" dentro de "no funciona mal" o "error" en "sin error" disparan la regla igual. Es una limitación aceptada de un sistema simple; la lista exacta sale de CLARIFY.
- **Mayúsculas y tildes:** "CAÍDO" o "caido" pueden no matchear si no se normaliza el texto. Se define en CLARIFY.
- **Ticket existente con la palabra "caído":** el test actual `"Login caído"` va a quedar en prioridad alta. No rompe nada, pero confirma que el título participa (si así se decide).

## Dependencias
- Ninguna dependencia externa: solo stdlib (`unicodedata` si hay que normalizar tildes).
- Depende de las respuestas de CLARIFY: lista de palabras clave, definición de VIP y formato del motivo.
