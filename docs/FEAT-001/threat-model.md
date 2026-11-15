# Threat model · FEAT-001 · Prioridad automática de tickets

| Categoría | Amenaza | Mitigación |
|---|---|---|
| Spoofing | Un cliente se hace pasar por VIP para que su ticket suba de prioridad. | La condición VIP no sale del texto que escribe el cliente: viene de un dato del sistema (campo o lista interna), y nunca de una palabra en la descripción. |
| Tampering | Un cliente mete palabras como "urgente" o "caído" para manipular la prioridad. | Es un riesgo aceptado del diseño por palabras clave. El motivo registrado muestra qué palabra disparó la regla, así soporte puede detectar el abuso. |
| Repudiation | Nadie puede explicar por qué un ticket quedó con cierta prioridad. | Toda asignación guarda un `motivo_prioridad` no vacío con la regla aplicada (RF-07). |
| Denial of service | Una descripción enorme hace lenta la búsqueda de palabras clave. | La búsqueda es lineal sobre una lista chica y fija de palabras (substring con `in`), sin regex con backtracking. |
| Information disclosure | El motivo expone datos internos (ej. que el cliente es VIP) si se le muestra al cliente. | El motivo es para el equipo de soporte; este cambio no lo expone en ninguna interfaz para clientes. |
