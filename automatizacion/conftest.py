"""Fixtures compartidos: configuración por .env y login por rol.

Para reducir la carga sobre Moodle (instancia local en Docker), cada rol inicia
sesión UNA sola vez por corrida y la cookie de sesión se reutiliza en los demás
tests. El login además espera solo el 'commit' de la navegación y reintenta
una vez si Moodle tarda en responder.
"""
import os
import pytest
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:8085").rstrip("/")
COURSE_ID = os.getenv("COURSE_ID", "2")
ASSIGN_CMID = os.getenv("ASSIGN_CMID", "3")

CREDENTIALS = {
    "admin": (os.getenv("ADMIN_USER"), os.getenv("ADMIN_PASS")),
    "docente": (os.getenv("TEACHER_USER"), os.getenv("TEACHER_PASS")),
    "estudiante": (os.getenv("STUDENT_USER"), os.getenv("STUDENT_PASS")),
}

_SESSION_COOKIES = {}  # rol -> cookies de sesión ya autenticadas


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def ids():
    return {"course": COURSE_ID, "assign": ASSIGN_CMID}


def _login_por_formulario(page, user, password):
    page.goto(f"{BASE_URL}/login/index.php", wait_until="domcontentloaded", timeout=60000)
    page.fill("#username", user)
    page.fill("#password", password)
    page.click("#loginbtn")
    page.wait_for_url(
        lambda url: "/login/" not in url, wait_until="commit", timeout=60000
    )


def do_login(page, role):
    user, password = CREDENTIALS[role]
    if not user or not password:
        pytest.skip(f"Faltan credenciales de '{role}' en .env")

    if role in _SESSION_COOKIES:
        page.context.add_cookies(_SESSION_COOKIES[role])
        page.goto(f"{BASE_URL}/my/", wait_until="domcontentloaded", timeout=60000)
        return

    for intento in (1, 2):
        try:
            _login_por_formulario(page, user, password)
            break
        except Exception:
            if intento == 2:
                raise
            page.context.clear_cookies()
    _SESSION_COOKIES[role] = page.context.cookies()


@pytest.fixture
def login(page):
    """Uso: login('docente') deja la sesión iniciada en la página."""
    def _login(role):
        do_login(page, role)
    return _login
