"""E2E por rol sobre Moodle (10 pruebas; cubren TC-001, 004, 005, 006, 007, 011, 012, 015 y 019)."""
import re
import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.e2e


def test_e2e_01_login_invalido_muestra_error(page, base_url):
    """TC-019: credenciales inválidas son rechazadas con mensaje claro."""
    page.goto(f"{base_url}/login/index.php")
    page.fill("#username", "estudiante.qa")
    page.fill("#password", "ClaveIncorrecta-123")
    page.click("#loginbtn")
    expect(page.locator(".alert-danger")).to_contain_text("Unable to log in")
    expect(page).to_have_url(re.compile(r"/login/"))


@pytest.mark.parametrize("rol", ["admin", "docente", "estudiante"])
def test_e2e_02_login_valido_por_rol(page, login, rol):
    """TC-001 (estudiante) y TC-005 (docente): cada rol inicia sesión y llega a su panel."""
    login(rol)
    expect(page).not_to_have_url(re.compile(r"/login/"))
    expect(page.locator("#user-menu-toggle, .usermenu").first).to_be_visible()


def test_e2e_03_estudiante_no_accede_a_administracion(page, login, base_url):
    """TC-004: el estudiante no puede abrir la administración del sitio."""
    login("estudiante")
    page.goto(f"{base_url}/admin/search.php")
    expect(
        page.get_by_text(re.compile("Access denied|do not currently have permissions", re.I)).first
    ).to_be_visible()


def test_e2e_04_estudiante_no_edita_el_curso(page, login, base_url, ids):
    """TC-015: el estudiante no puede editar la configuración del curso."""
    login("estudiante")
    page.goto(f"{base_url}/course/edit.php?id={ids['course']}")
    expect(
        page.get_by_text(re.compile("Access denied|do not currently have permissions|Sorry", re.I)).first
    ).to_be_visible()


def test_e2e_05_docente_ve_participantes(page, login, base_url, ids):
    """TC-007: el docente consulta la lista de participantes del curso."""
    login("docente")
    page.goto(f"{base_url}/user/index.php?id={ids['course']}")
    expect(page.get_by_text("Estudiante Prueba").first).to_be_visible()


def test_e2e_06_docente_no_accede_a_administracion(page, login, base_url):
    """TC-006: el docente no tiene acceso a la administración del sitio."""
    login("docente")
    page.goto(f"{base_url}/admin/search.php")
    expect(
        page.get_by_text(re.compile("Access denied|do not currently have permissions", re.I)).first
    ).to_be_visible()


def test_e2e_07_estudiante_ve_nota_y_retroalimentacion(page, login, base_url, ids):
    """TC-011: el estudiante ve su nota 85/100 y el comentario del docente."""
    login("estudiante")
    page.goto(f"{base_url}/mod/assign/view.php?id={ids['assign']}")
    expect(page.get_by_text("85.00 / 100.00")).to_be_visible()
    expect(page.get_by_text("Buen análisis")).to_be_visible()


def test_e2e_08_calificador_rechaza_nota_mayor_a_100(page, login, base_url, ids):
    """TC-012: el docente no puede guardar una nota de 150 (máximo 100)."""
    login("docente")
    page.goto(f"{base_url}/mod/assign/view.php?id={ids['assign']}&action=grader&userid=4")
    campo = page.get_by_label(re.compile(r"Grade out of 100"))
    campo.fill("150")
    page.get_by_role("button", name="Save changes").click()
    expect(page.get_by_text(re.compile("less than or equal to 100")).first).to_be_visible()
    # La nota válida previa (85) no se debe perder.
    page.goto(f"{base_url}/mod/assign/view.php?id={ids['assign']}&action=grader&userid=4")
    expect(page.get_by_label(re.compile(r"Grade out of 100"))).to_have_value(re.compile(r"^85"))
