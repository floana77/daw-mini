# Clarificaciones · FEAT-001
- **P1:** ¿Qué palabras clave disparan cada nivel y dónde se buscan?
  - **R:** En título + descripción, por familias de expresiones según intención. Alta: caído, se cayó, no funciona, no anda, no puedo entrar, urgente, crítico, bloqueado. Media: lento, tarda, demora, error, falla.
- **P2:** ¿Se ignoran mayúsculas y tildes?
  - **R:** Sí, se ignoran mayúsculas y tildes.
- **P3:** Si un ticket matchea alta y media, ¿qué prioridad queda?
  - **R:** Gana la más alta.
- **P4:** ¿Cómo se sabe que un cliente es VIP?
  - **R:** Lista fija en el código: `acme` y `globex`.
- **P5:** ¿Cuánto se le sube la prioridad a un VIP?
  - **R:** Sube un nivel; si ya era alta, queda en alta.
- **P6:** ¿Qué formato tiene el motivo?
  - **R:** Corto, del tipo `"media: matcheó 'lenta'; +1 por cliente VIP"`, sin copiar texto libre del ticket.

## Interpretaciones del orquestador (a validar en el checkpoint de SPEC)
- "Familias de expresiones": cada familia incluye sus variantes de género (caído/caída, crítico/crítica, bloqueado/bloqueada, lento/lenta), porque el ejemplo de P6 cita 'lenta'. El match es por substring sobre el texto normalizado, así que los plurales entran solos (ej. "errores", "fallas").
- El motivo cita la expresión de la lista fija, nunca texto del ticket. Si matchean varias, cita la primera de la lista del nivel ganador.
- El prefijo del motivo es el nivel que dan las palabras clave, sin contar el ajuste VIP; el `+1` va aparte, como en el ejemplo de P6.
- Sin coincidencias, el motivo es `"baja: no matcheó ninguna expresión"`.
- El nombre del cliente se compara contra la lista VIP sin distinguir mayúsculas.
