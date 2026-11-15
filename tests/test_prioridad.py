import sys, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from tickettriage.tickets import crear_ticket

HORARIO = "Quisiera saber el horario de atención"
LENTA = "La página anda muy lenta"
CAIDO = "El sistema de facturación está caído"


class TestPrioridad(unittest.TestCase):
    def test_ac01_toda_prioridad_es_valida(self):
        """AC-01: todo ticket nuevo tiene prioridad alta, media o baja."""
        t = crear_ticket("Consulta", HORARIO, "initech")
        self.assertIn(t.prioridad, {"alta", "media", "baja"})

    def test_ac02_ignora_mayusculas_y_tildes_en_titulo(self):
        """AC-02: 'Servidor CAIDO' en el título da alta."""
        t = crear_ticket("Servidor CAIDO", "por favor revisar", "initech")
        self.assertEqual(t.prioridad, "alta")

    def test_ac03_caido_da_alta(self):
        """AC-03: 'está caído' da alta."""
        t = crear_ticket("Facturación", CAIDO, "initech")
        self.assertEqual(t.prioridad, "alta")

    def test_ac04_no_puedo_entrar_da_alta(self):
        """AC-04: 'No puedo entrar' da alta."""
        t = crear_ticket("Acceso", "No puedo entrar a mi cuenta", "initech")
        self.assertEqual(t.prioridad, "alta")

    def test_ac05_lenta_da_media(self):
        """AC-05: 'anda muy lenta' da media."""
        t = crear_ticket("Reportes", LENTA, "initech")
        self.assertEqual(t.prioridad, "media")

    def test_ac06_error_da_media(self):
        """AC-06: 'tira error' da media."""
        t = crear_ticket("Guardar", "Al guardar me tira error", "initech")
        self.assertEqual(t.prioridad, "media")

    def test_ac07_sin_expresiones_da_baja(self):
        """AC-07: sin expresiones clave y no VIP da baja."""
        t = crear_ticket("Consulta", HORARIO, "initech")
        self.assertEqual(t.prioridad, "baja")

    def test_ac08_alta_gana_sobre_media(self):
        """AC-08: 'caído y tira error' da alta."""
        t = crear_ticket("Login", "El login está caído y tira error", "initech")
        self.assertEqual(t.prioridad, "alta")

    def test_ac09_vip_mayusculas_sube_baja_a_media(self):
        """AC-09: cliente 'ACME' sin expresiones da media."""
        t = crear_ticket("Consulta", HORARIO, "ACME")
        self.assertEqual(t.prioridad, "media")

    def test_ac10_vip_sube_media_a_alta(self):
        """AC-10: cliente 'globex' con 'lenta' da alta."""
        t = crear_ticket("Reportes", LENTA, "globex")
        self.assertEqual(t.prioridad, "alta")

    def test_ac11_vip_alta_queda_alta(self):
        """AC-11: cliente 'acme' con 'caído' queda en alta."""
        t = crear_ticket("Facturación", CAIDO, "acme")
        self.assertEqual(t.prioridad, "alta")

    def test_ac12_acme_corp_no_es_vip(self):
        """AC-12: cliente 'acme corp' no es VIP: 'lenta' da media."""
        t = crear_ticket("Reportes", LENTA, "acme corp")
        self.assertEqual(t.prioridad, "media")

    def test_ac13_motivo_con_vip(self):
        """AC-13: motivo exacto con ajuste VIP."""
        t = crear_ticket("Reportes", LENTA, "globex")
        self.assertEqual(t.motivo_prioridad, "media: matcheó 'lenta'; +1 por cliente VIP")

    def test_ac14_motivo_alta(self):
        """AC-14: motivo exacto para 'caído'."""
        t = crear_ticket("Facturación", CAIDO, "initech")
        self.assertEqual(t.motivo_prioridad, "alta: matcheó 'caído'")

    def test_ac15_motivo_sin_coincidencias(self):
        """AC-15: motivo exacto sin coincidencias."""
        t = crear_ticket("Consulta", HORARIO, "initech")
        self.assertEqual(t.motivo_prioridad, "baja: no matcheó ninguna expresión")

    def test_ac16_motivo_no_copia_texto_del_ticket(self):
        """AC-16: el motivo cita la lista fija y no copia texto libre."""
        t = crear_ticket("Ayuda", "URGENTE!!! mi clave secreta es 1234", "initech")
        self.assertEqual(t.motivo_prioridad, "alta: matcheó 'urgente'")
        self.assertNotIn("1234", t.motivo_prioridad)


if __name__ == "__main__":
    unittest.main()
