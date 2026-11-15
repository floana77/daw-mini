# PRD · FEAT-001 · Prioridad automática de tickets
## Contexto
Hoy, cuando entra un ticket en TicketTriage, alguien del equipo de soporte lo lee y decide a mano si es urgente. Eso lleva tiempo, y muchas veces los tickets importantes quedan abajo de la pila.

## Objetivo
Que todo ticket nuevo reciba de forma automática una prioridad (alta, media o baja), con reglas simples, deterministas y sin IA, y que el equipo pueda ver por qué se le asignó esa prioridad.

## Requerimientos funcionales
- **RF-01** El sistema debe asignar una prioridad (`alta`, `media` o `baja`) a todo ticket en el momento de su creación.
- **RF-02** El sistema debe buscar las expresiones clave en el título y en la descripción del ticket, sin distinguir mayúsculas ni tildes.
- **RF-03** El sistema debe asignar nivel `alta` cuando el texto contenga alguna de estas expresiones: "caído", "caída", "se cayó", "no funciona", "no anda", "no puedo entrar", "urgente", "crítico", "crítica", "bloqueado", "bloqueada".
- **RF-04** El sistema debe asignar nivel `media` cuando el texto contenga alguna de estas expresiones: "lento", "lenta", "tarda", "demora", "error", "falla".
- **RF-05** El sistema debe asignar nivel `baja` cuando el texto no contenga ninguna expresión de alta ni de media.
- **RF-06** El sistema debe quedarse con el nivel más alto cuando el texto contenga expresiones de más de un nivel.
- **RF-07** El sistema debe considerar VIP únicamente a los clientes de una lista fija en el código: `acme` y `globex`, comparados sin distinguir mayúsculas.
- **RF-08** El sistema debe subir un nivel la prioridad de los tickets de clientes VIP (baja → media, media → alta), y dejar en `alta` a los que ya eran alta.
- **RF-09** El sistema debe registrar en el ticket un motivo con el formato `"<nivel por expresiones>: matcheó '<expresión>'"` y, si es VIP, el agregado `"; +1 por cliente VIP"`. La expresión citada es la primera de la lista del nivel ganador que aparece en el texto.
- **RF-10** El sistema debe registrar el motivo `"baja: no matcheó ninguna expresión"` (más `"; +1 por cliente VIP"` si corresponde) cuando no haya coincidencias.
- **RF-11** El motivo no debe incluir texto libre del ticket: solo el nivel, la expresión de la lista fija y el ajuste VIP.

## Criterios de aceptación
- **AC-01** (RF-01) Dado un ticket con título "Consulta", descripción "Quisiera saber el horario de atención" y cliente "initech", cuando se crea, entonces su prioridad es una de `alta`, `media` o `baja`.
- **AC-02** (RF-02) Dado un ticket con título "Servidor CAIDO" y descripción "por favor revisar", de cliente "initech", cuando se crea, entonces su prioridad es `alta`.
- **AC-03** (RF-03) Dado un ticket con título "Facturación" y descripción "El sistema de facturación está caído", de cliente "initech", cuando se crea, entonces su prioridad es `alta`.
- **AC-04** (RF-03) Dado un ticket con título "Acceso" y descripción "No puedo entrar a mi cuenta", de cliente "initech", cuando se crea, entonces su prioridad es `alta`.
- **AC-05** (RF-04) Dado un ticket con título "Reportes" y descripción "La página anda muy lenta", de cliente "initech", cuando se crea, entonces su prioridad es `media`.
- **AC-06** (RF-04) Dado un ticket con título "Guardar" y descripción "Al guardar me tira error", de cliente "initech", cuando se crea, entonces su prioridad es `media`.
- **AC-07** (RF-05) Dado un ticket con título "Consulta" y descripción "Quisiera saber el horario de atención", de cliente "initech", cuando se crea, entonces su prioridad es `baja`.
- **AC-08** (RF-06) Dado un ticket con título "Login" y descripción "El login está caído y tira error", de cliente "initech", cuando se crea, entonces su prioridad es `alta`.
- **AC-09** (RF-08) Dado un ticket con título "Consulta" y descripción "Quisiera saber el horario de atención", de cliente "ACME", cuando se crea, entonces su prioridad es `media`.
- **AC-10** (RF-08) Dado un ticket con título "Reportes" y descripción "La página anda muy lenta", de cliente "globex", cuando se crea, entonces su prioridad es `alta`.
- **AC-11** (RF-08) Dado un ticket con título "Facturación" y descripción "El sistema de facturación está caído", de cliente "acme", cuando se crea, entonces su prioridad es `alta`.
- **AC-12** (RF-07) Dado un ticket con título "Reportes" y descripción "La página anda muy lenta", de cliente "acme corp", cuando se crea, entonces su prioridad es `media`.
- **AC-13** (RF-09) Dado un ticket con título "Reportes" y descripción "La página anda muy lenta", de cliente "globex", cuando se crea, entonces su motivo es exactamente `"media: matcheó 'lenta'; +1 por cliente VIP"`.
- **AC-14** (RF-09) Dado un ticket con título "Facturación" y descripción "El sistema de facturación está caído", de cliente "initech", cuando se crea, entonces su motivo es exactamente `"alta: matcheó 'caído'"`.
- **AC-15** (RF-10) Dado un ticket con título "Consulta" y descripción "Quisiera saber el horario de atención", de cliente "initech", cuando se crea, entonces su motivo es exactamente `"baja: no matcheó ninguna expresión"`.
- **AC-16** (RF-11) Dado un ticket con título "Ayuda" y descripción "URGENTE!!! mi clave secreta es 1234", de cliente "initech", cuando se crea, entonces su motivo es exactamente `"alta: matcheó 'urgente'"` y no contiene "1234".

## Fuera de alcance
- Cambiar la prioridad con el tiempo si nadie atiende el ticket (escalado por antigüedad).
- Usar IA o modelos de lenguaje para clasificar.
- Agregar dependencias externas.
- Administrar la lista de clientes VIP fuera del código (base de datos, configuración, UI).
