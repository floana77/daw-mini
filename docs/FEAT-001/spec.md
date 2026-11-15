# Spec · FEAT-001 · Prioridad automática de tickets

## Diseño
- **Nuevo módulo `src/tickettriage/prioridad.py`**, con funciones puras y deterministas, sin estado y solo stdlib (`unicodedata`).
  - Tuplas ordenadas de expresiones, escritas con tildes para poder citarlas en el motivo:
    - `EXPRESIONES_ALTA = ("caído", "caída", "se cayó", "no funciona", "no anda", "no puedo entrar", "urgente", "crítico", "crítica", "bloqueado", "bloqueada")`
    - `EXPRESIONES_MEDIA = ("lento", "lenta", "tarda", "demora", "error", "falla")`
  - `CLIENTES_VIP = frozenset({"acme", "globex"})`.
  - `NIVELES = ("baja", "media", "alta")`: el índice define el orden para subir un nivel.
  - **Normalización (RF-02):** `normalizar(texto)` pasa a minúsculas, descompone con NFD y descarta las marcas combinantes (categoría `Mn`). Se aplica al texto del ticket y a cada expresión antes de comparar.
  - **Texto a evaluar:** `titulo + "\n" + descripcion`. El separador evita matches que crucen el borde entre título y descripción.
  - **Match:** substring (`in`) de la expresión normalizada en el texto normalizado, sin regex. Los plurales entran solos ("errores" contiene "error").
  - **Nivel por expresiones (RF-03 a RF-06):** primero se recorre `EXPRESIONES_ALTA` en orden; la primera que aparezca da `alta` y es la que se cita. Si ninguna aparece, se recorre `EXPRESIONES_MEDIA` de la misma forma. Si tampoco, queda `baja` sin expresión. Con este orden gana el nivel más alto.
  - **VIP (RF-07, RF-08):** `es_vip(cliente)` normaliza `cliente.strip()` y lo busca en `CLIENTES_VIP` (match exacto: "acme corp" no es VIP). Si es VIP, se sube el nivel con `NIVELES[min(i + 1, 2)]`.
  - **Motivo (RF-09 a RF-11):** se arma solo con el nivel por expresiones (antes de VIP), la expresión de la lista fija y el sufijo VIP:
    - `"<nivel>: matcheó '<expresión>'"` o `"baja: no matcheó ninguna expresión"`
    - más `"; +1 por cliente VIP"` si corresponde.
    Nunca se interpola texto del ticket.
- **Cambios en `src/tickettriage/tickets.py`:**
  - `Ticket` suma `prioridad: str = "baja"` y `motivo_prioridad: str = ""`. Tienen default para no romper a quien construya `Ticket` directo.
  - `crear_ticket` mantiene su firma y, después de validar y limpiar, llama a `calcular_prioridad` y guarda ambos campos (RF-01).

## Interfaz
```python
# src/tickettriage/prioridad.py
NIVELES: tuple[str, ...]            # ("baja", "media", "alta")
EXPRESIONES_ALTA: tuple[str, ...]
EXPRESIONES_MEDIA: tuple[str, ...]
CLIENTES_VIP: frozenset[str]        # {"acme", "globex"}

def normalizar(texto: str) -> str: ...
def es_vip(cliente: str) -> bool: ...
def calcular_prioridad(titulo: str, descripcion: str, cliente: str) -> tuple[str, str]:
    """Devuelve (prioridad, motivo)."""

# src/tickettriage/tickets.py
@dataclass
class Ticket:
    titulo: str
    descripcion: str
    cliente: str
    creado: datetime = ...
    prioridad: str = "baja"
    motivo_prioridad: str = ""

def crear_ticket(titulo: str, descripcion: str, cliente: str) -> Ticket: ...  # firma sin cambios
```

## Plan de tests
Archivo nuevo: `tests/test_prioridad.py`. Todos los casos van por `crear_ticket(titulo, descripcion, cliente)` y verifican `t.prioridad` / `t.motivo_prioridad`. Los tests de `tests/test_tickets.py` se mantienen.
- AC-01: ("Consulta", "Quisiera saber el horario de atención", "initech") → `prioridad in {"alta", "media", "baja"}`.
- AC-02: ("Servidor CAIDO", "por favor revisar", "initech") → `alta` (mayúsculas y sin tilde, en el título).
- AC-03: ("Facturación", "El sistema de facturación está caído", "initech") → `alta`.
- AC-04: ("Acceso", "No puedo entrar a mi cuenta", "initech") → `alta`.
- AC-05: ("Reportes", "La página anda muy lenta", "initech") → `media`.
- AC-06: ("Guardar", "Al guardar me tira error", "initech") → `media`.
- AC-07: ("Consulta", "Quisiera saber el horario de atención", "initech") → `baja`.
- AC-08: ("Login", "El login está caído y tira error", "initech") → `alta`.
- AC-09: ("Consulta", "Quisiera saber el horario de atención", "ACME") → `media`.
- AC-10: ("Reportes", "La página anda muy lenta", "globex") → `alta`.
- AC-11: ("Facturación", "El sistema de facturación está caído", "acme") → `alta`.
- AC-12: ("Reportes", "La página anda muy lenta", "acme corp") → `media`.
- AC-13: ("Reportes", "La página anda muy lenta", "globex") → motivo == `"media: matcheó 'lenta'; +1 por cliente VIP"`.
- AC-14: ("Facturación", "El sistema de facturación está caído", "initech") → motivo == `"alta: matcheó 'caído'"`.
- AC-15: ("Consulta", "Quisiera saber el horario de atención", "initech") → motivo == `"baja: no matcheó ninguna expresión"`.
- AC-16: ("Ayuda", "URGENTE!!! mi clave secreta es 1234", "initech") → motivo == `"alta: matcheó 'urgente'"` y `"1234" not in motivo`.
