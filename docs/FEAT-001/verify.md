# Verify · FEAT-001 · Prioridad automática de tickets

Auditoría independiente. Suite corrida desde la raíz con `python3 -m unittest discover -s tests -t .`: **18 tests, OK** (16 de `test_prioridad.py` + 2 de `test_tickets.py`).

| AC | Test | OK |
|---|---|---|
| AC-01 | `test_ac01_toda_prioridad_es_valida` | Sí |
| AC-02 | `test_ac02_ignora_mayusculas_y_tildes_en_titulo` | Sí |
| AC-03 | `test_ac03_caido_da_alta` | Sí |
| AC-04 | `test_ac04_no_puedo_entrar_da_alta` | Sí |
| AC-05 | `test_ac05_lenta_da_media` | Sí |
| AC-06 | `test_ac06_error_da_media` | Sí |
| AC-07 | `test_ac07_sin_expresiones_da_baja` | Sí |
| AC-08 | `test_ac08_alta_gana_sobre_media` | Sí |
| AC-09 | `test_ac09_vip_mayusculas_sube_baja_a_media` | Sí |
| AC-10 | `test_ac10_vip_sube_media_a_alta` | Sí |
| AC-11 | `test_ac11_vip_alta_queda_alta` | Sí |
| AC-12 | `test_ac12_acme_corp_no_es_vip` | Sí |
| AC-13 | `test_ac13_motivo_con_vip` | Sí |
| AC-14 | `test_ac14_motivo_alta` | Sí |
| AC-15 | `test_ac15_motivo_sin_coincidencias` | Sí |
| AC-16 | `test_ac16_motivo_no_copia_texto_del_ticket` | Sí |

## Hallazgos

- **Cobertura de AC:** los 16 AC tienen un test propio que usa los datos exactos del PRD y pasa por `crear_ticket` (la API pública), así que se prueba la integración y no solo la función pura. Las aserciones son de igualdad exacta (`assertEqual`) sobre `prioridad` y `motivo_prioridad`, no triviales.
- **AC-01:** el test solo chequea pertenencia a `{"alta","media","baja"}`, que es lo que pide el AC. Es débil por cómo está escrito el AC, no por el test; igual el mismo caso queda cubierto con valor exacto en AC-07 y AC-15.
- **Código vs. spec:** `src/tickettriage/prioridad.py` sigue la spec al pie: tuplas ordenadas con tildes, normalización NFD descartando `Mn`, texto `titulo + "\n" + descripcion`, match por substring sin regex, alta antes que media (RF-06), VIP por match exacto sobre `cliente.strip()` normalizado, y motivo armado solo con nivel por expresiones + expresión de la lista fija + sufijo VIP. `crear_ticket` mantiene la firma y asigna ambos campos después de validar y limpiar (RF-01).
- **Menor (no bloqueante):** `es_vip` además de ignorar mayúsculas ignora tildes (`" Ácme "` es VIP). RF-07 solo dice "sin distinguir mayúsculas"; la spec lo define así a propósito y no contradice ningún AC.
- **Menor (no bloqueante):** el match por substring da falsos positivos (ej.: "fue violento" → `media: matcheó 'lento'`). Es consecuencia aceptada del diseño de la spec; vale tenerlo en cuenta para una iteración futura (límites de palabra).
- **Menor (no bloqueante):** `Ticket` construido directo (sin `crear_ticket`) queda con `prioridad="baja"` y `motivo_prioridad=""`. La spec lo acepta por compatibilidad, pero la mitigación de Repudiation ("todo motivo no vacío") solo vale para tickets creados con `crear_ticket`.
- **Threat model:**
  - Spoofing: mitigado. VIP sale solo del campo `cliente` contra `CLIENTES_VIP` fijo en el código; la descripción no influye.
  - Tampering: riesgo aceptado; el motivo cita la expresión que disparó la regla (verificado en AC-13/14/16).
  - Repudiation: mitigado para todo ticket creado vía `crear_ticket` (siempre hay motivo no vacío). Detalle de doc: el threat model referencia RF-07, pero el motivo corresponde a RF-09/RF-10.
  - Denial of service: mitigado. Búsqueda lineal con `in` sobre 17 expresiones fijas, sin regex; probé título y descripción de 5 MB cada uno y tardó ~0,9 s.
  - Information disclosure: este cambio no expone `motivo_prioridad` en ninguna interfaz para clientes (no hay interfaz en el repo). Además el motivo nunca interpola texto libre (AC-16).
- **Sin dependencias externas:** solo stdlib (`unicodedata`, `dataclasses`, `datetime`), en línea con el fuera de alcance.

VEREDICTO: APROBADO
