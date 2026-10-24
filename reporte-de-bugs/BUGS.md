# Reporte de defectos — Proyecto 7 (Moodle 5.2.4)

Solo se reportan defectos confirmados con evidencia. Las observaciones de mejora están al final y no se consideran defectos.

## BUG-001 — La línea «Due date» del encabezado del calificador aparece cortada

| Campo | Detalle |
|---|---|
| Severidad | Baja (cosmético) |
| Prioridad | Baja |
| Ambiente | Moodle 5.2.4 (build 20261005), MariaDB 11.4.13, PHP 8.4.26; Opera y Microsoft Edge (Chromium) en Windows, 1920 × 1080. |

**Precondiciones:** Docente con sesión iniciada; entrega del estudiante enviada en Reflexión 2.

**Pasos para reproducir**
1. Iniciar sesión como docente.qa.
2. Abrir Reflexión 2 > View all submissions > Grade (o la URL /mod/assign/view.php?id=3&action=grader&userid=4).
3. Observar el encabezado con el nombre y el correo del estudiante.

**Resultado esperado:** La línea «Due date: 30 October 2026, 11:59 PM» se ve completa debajo del correo del estudiante.

**Resultado obtenido:** La línea queda cortada por la mitad. Se reproduce en Opera y en Microsoft Edge, también con el zoom reducido. Además, cuando una validación falla (TC-012), el aviso rojo se superpone al nombre y al correo del estudiante.

**Evidencia:** P7_BUG-001_docente_encabezado-fecha-cortada.png, P7_BUG-001_docente_encabezado-fecha-cortada-zoom-reducido.png y P7_TC-012_docente_nota-150-rechazada.png

**Nota:** Se probó en una sola resolución; no se verificó en pantallas más pequeñas.

---

## BUG-002 — El separador «Resize layout» del calificador usa aria-label sin un rol válido

| Campo | Detalle |
|---|---|
| Severidad | Media (accesibilidad; impacto «serious» en axe-core) |
| Prioridad | Baja |
| Ambiente | Moodle 5.2.4; axe-core 4.12 vía axe-playwright-python; Chromium (Playwright 0.10); Windows. |

**Precondiciones:** Docente con sesión iniciada; calificador abierto para una entrega.

**Pasos para reproducir**
1. Iniciar sesión como docente.qa.
2. Abrir el calificador de Reflexión 2.
3. Ejecutar el escaneo axe-core (prueba test_a11y_05_calificador_docente) con las etiquetas WCAG 2.0/2.1 A y AA.

**Resultado esperado:** El elemento usa solo atributos ARIA permitidos para su rol, de modo que un lector de pantalla lo anuncie correctamente (WCAG 4.1.2).

**Resultado obtenido:** Regla aria-prohibited-attr (1 elemento): <div data-region="resizer" tabindex="0" aria-label="Resize layout" title="Resize layout"></div>. Un div sin rol no admite aria-label. La causa es una inferencia a partir de la regla de axe-core, sin revisar el código fuente.

**Evidencia:** P7_AUTO_axe-violaciones.png y automatizacion/reports/axe_05_calificador_docente.json

**Nota:** Es componente del núcleo de Moodle: lo adecuado sería reportarlo en el tracker de Moodle tras verificar que no exista ya.

---

## BUG-003 — La región desplazable del calificador (.drawingregion) no es accesible con teclado

| Campo | Detalle |
|---|---|
| Severidad | Media (accesibilidad; impacto «serious» en axe-core) |
| Prioridad | Media |
| Ambiente | Moodle 5.2.4; axe-core 4.12 vía axe-playwright-python; Chromium (Playwright 0.10); Windows. |

**Precondiciones:** Docente con sesión iniciada; calificador abierto para una entrega.

**Pasos para reproducir**
1. Iniciar sesión como docente.qa.
2. Abrir el calificador de Reflexión 2.
3. Ejecutar el escaneo axe-core (test_a11y_05_calificador_docente).

**Resultado esperado:** Toda región con desplazamiento es alcanzable y operable con el teclado (WCAG 2.1.1 y 2.1.3).

**Resultado obtenido:** Regla scrollable-region-focusable (1 elemento): <div class="drawingregion" data-currenttool="drag">. Una persona que no usa ratón no puede desplazar ese contenido. No se comprobó a mano con teclado; el hallazgo proviene del escaneo automatizado.

**Evidencia:** P7_AUTO_axe-violaciones.png y automatizacion/reports/axe_05_calificador_docente.json

**Nota:** Pendiente: confirmar con una prueba manual de teclado (tabulador) para descartar un falso positivo.

---

## Observaciones de mejora

| ID | Área | Observación | Siguiente paso |
|---|---|---|---|
| O-1 | Privacidad (TC-008) | El estudiante ve el último acceso al curso del docente y del administrador en la lista de participantes. | Revisar el ajuste «Hide user fields» y decidir si se oculta a estudiantes. |
| O-2 | Validación (TC-017) | Moodle acepta una fecha límite ya vencida sin advertencia al crear la tarea. | Considerar un aviso para evitar errores de captura del docente. |
| O-3 | Localización (entorno) | La interfaz está en inglés y el contenido del curso en español; la imagen no tiene el idioma configurado. | Establecer MOODLE_LANG=es en el entorno y repetir la revisión de textos. |
| O-4 | Notificaciones (sin verificar) | El contador de la campana del estudiante aumentó durante las pruebas hasta 7. | No se investigó su causa; no se reporta como defecto. Revisar en una siguiente iteración. |
