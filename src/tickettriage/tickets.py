"""Alta de tickets de soporte."""
from dataclasses import dataclass, field
from datetime import datetime, timezone

from .prioridad import calcular_prioridad


@dataclass
class Ticket:
    titulo: str
    descripcion: str
    cliente: str
    creado: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    prioridad: str = "baja"
    motivo_prioridad: str = ""


def crear_ticket(titulo: str, descripcion: str, cliente: str) -> Ticket:
    if not titulo.strip():
        raise ValueError("El título es obligatorio")
    titulo, descripcion, cliente = titulo.strip(), descripcion.strip(), cliente.strip()
    prioridad, motivo = calcular_prioridad(titulo, descripcion, cliente)
    return Ticket(
        titulo=titulo,
        descripcion=descripcion,
        cliente=cliente,
        prioridad=prioridad,
        motivo_prioridad=motivo,
    )
