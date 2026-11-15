"""Prioridad automática de tickets: funciones puras y deterministas."""
import unicodedata

NIVELES = ("baja", "media", "alta")

EXPRESIONES_ALTA = (
    "caído", "caída", "se cayó", "no funciona", "no anda", "no puedo entrar",
    "urgente", "crítico", "crítica", "bloqueado", "bloqueada",
)
EXPRESIONES_MEDIA = ("lento", "lenta", "tarda", "demora", "error", "falla")

CLIENTES_VIP = frozenset({"acme", "globex"})


def normalizar(texto: str) -> str:
    """Minúsculas y sin tildes (NFD, descarta marcas combinantes)."""
    descompuesto = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in descompuesto if unicodedata.category(c) != "Mn")


def es_vip(cliente: str) -> bool:
    return normalizar(cliente.strip()) in CLIENTES_VIP


def _primera_expresion(texto: str, expresiones: tuple[str, ...]) -> str | None:
    for expresion in expresiones:
        if normalizar(expresion) in texto:
            return expresion
    return None


def calcular_prioridad(titulo: str, descripcion: str, cliente: str) -> tuple[str, str]:
    """Devuelve (prioridad, motivo)."""
    texto = normalizar(titulo + "\n" + descripcion)

    expresion = _primera_expresion(texto, EXPRESIONES_ALTA)
    if expresion is not None:
        nivel = "alta"
    else:
        expresion = _primera_expresion(texto, EXPRESIONES_MEDIA)
        nivel = "media" if expresion is not None else "baja"

    if expresion is not None:
        motivo = f"{nivel}: matcheó '{expresion}'"
    else:
        motivo = "baja: no matcheó ninguna expresión"

    prioridad = nivel
    if es_vip(cliente):
        prioridad = NIVELES[min(NIVELES.index(nivel) + 1, len(NIVELES) - 1)]
        motivo += "; +1 por cliente VIP"

    return prioridad, motivo
