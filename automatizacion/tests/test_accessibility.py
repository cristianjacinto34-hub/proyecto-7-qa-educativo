"""Accesibilidad automatizada con axe-core (WCAG 2.x A/AA) en páginas clave."""
import json
import pathlib
import pytest
from axe_playwright_python.sync_playwright import Axe

pytestmark = pytest.mark.a11y
REPORTS = pathlib.Path("reports")
WCAG_TAGS = {"runOnly": {"type": "tag", "values": ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"]}}


def escanear(page, nombre):
    resultado = Axe().run(page, options=WCAG_TAGS)
    violaciones = resultado.response["violations"]
    REPORTS.mkdir(exist_ok=True)
    resumen = [
        {
            "regla": v["id"],
            "impacto": v["impact"],
            "descripcion": v["help"],
            "elementos_afectados": len(v["nodes"]),
            "ayuda": v["helpUrl"],
            "wcag": [t for t in v.get("tags", []) if t.startswith("wcag") and t[4:].isdigit()],
            "elementos": [
                {"selector": " ".join(map(str, n["target"])), "html": n["html"][:200]}
                for n in v["nodes"][:3]
            ],
        }
        for v in violaciones
    ]
    (REPORTS / f"axe_{nombre}.json").write_text(
        json.dumps(resumen, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"\n[axe] {nombre}: {len(violaciones)} reglas incumplidas")
    for r in resumen:
        print(f"   - [{r['impacto']}] {r['regla']} ({r['elementos_afectados']} elementos)")
    return violaciones


def sin_criticas(violaciones):
    return [v["id"] for v in violaciones if v["impact"] == "critical"]


def test_a11y_01_login(page, base_url):
    page.goto(f"{base_url}/login/index.php")
    assert not sin_criticas(escanear(page, "01_login"))


def test_a11y_02_panel_estudiante(page, login, base_url):
    login("estudiante")
    page.goto(f"{base_url}/my/")
    page.wait_for_load_state("networkidle")
    assert not sin_criticas(escanear(page, "02_panel_estudiante"))


def test_a11y_03_curso_estudiante(page, login, base_url, ids):
    login("estudiante")
    page.goto(f"{base_url}/course/view.php?id={ids['course']}")
    page.wait_for_load_state("networkidle")
    assert not sin_criticas(escanear(page, "03_curso_estudiante"))


def test_a11y_04_tarea_estudiante(page, login, base_url, ids):
    login("estudiante")
    page.goto(f"{base_url}/mod/assign/view.php?id={ids['assign']}")
    page.wait_for_load_state("networkidle")
    assert not sin_criticas(escanear(page, "04_tarea_estudiante"))


def test_a11y_05_calificador_docente(page, login, base_url, ids):
    login("docente")
    page.goto(f"{base_url}/mod/assign/view.php?id={ids['assign']}&action=grader&userid=4")
    page.wait_for_load_state("networkidle")
    assert not sin_criticas(escanear(page, "05_calificador_docente"))
