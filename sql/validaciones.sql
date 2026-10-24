-- Validaciones SQL del Proyecto 7 (MariaDB, base `moodle`, prefijo mdl_)
-- Las fechas salen en UTC; Cancún es UTC-5.

-- 01. Tareas y fechas límite
-- Esperado: grade = 100 en ambas; vencimientos 14/10 05:00 y 31/10 04:59 (UTC), equivalentes a 14/10 00:00 y 30/10 23:59 en Cancún.
-- Resultado: Coincide (evidencia: P7_SQL_01_tareas-y-fechas-limite.png)
SELECT id, name, grade, FROM_UNIXTIME(duedate) AS fecha_limite FROM mdl_assign;

-- 02. Límite de palabras
-- Esperado: wordlimit = 100 y wordlimitenabled = 1 en las dos tareas.
-- Resultado: Coincide (evidencia: P7_SQL_02_limite-palabras.png)
SELECT assignment, plugin, subtype, name, value FROM mdl_assign_plugin_config WHERE name IN ('wordlimit','wordlimitenabled');

-- 03. Entregas del estudiante
-- Esperado: userid 4 con status submitted en ambas tareas; la entrega de la tarea 1 es posterior a su fecha límite.
-- Resultado: Coincide (evidencia: P7_SQL_03_entregas.png)
SELECT s.id, s.assignment, s.userid, s.status, FROM_UNIXTIME(s.timemodified) AS modificado FROM mdl_assign_submission s ORDER BY s.id;

-- 04. Nota guardada
-- Esperado: grade = 85 en la tarea 2; -1 (sin calificar) en la tarea 1. No existe rastro de 150 ni 101.
-- Resultado: Coincide (evidencia: P7_SQL_04_nota-85.png)
SELECT assignment, userid, grade, FROM_UNIXTIME(timemodified) AS calificado FROM mdl_assign_grades;

-- 05. Libro de calificaciones
-- Esperado: finalgrade = 85 sobre rawgrademax = 100 (ítem de la tarea y total del curso).
-- Resultado: Coincide (evidencia: P7_SQL_05_libro-calificaciones.png)
SELECT itemid, userid, finalgrade, rawgrademax FROM mdl_grade_grades WHERE finalgrade IS NOT NULL;

-- 06. Usuarios y roles
-- Esperado: docente.qa y admin con editingteacher; estudiante.qa con student; todos a nivel curso (50).
-- Resultado: Coincide (evidencia: P7_SQL_06_roles-asignados.png)
SELECT u.username, u.email, r.shortname AS rol, c.contextlevel FROM mdl_role_assignments ra JOIN mdl_user u ON u.id = ra.userid JOIN mdl_role r ON r.id = ra.roleid JOIN mdl_context c ON c.id = ra.contextid;

-- 07. Correos duplicados
-- Esperado: 0 filas: ningún correo repetido.
-- Resultado: Coincide (evidencia: P7_SQL_07_correos-duplicados-ninguno.png)
SELECT email, COUNT(*) AS veces FROM mdl_user GROUP BY email HAVING COUNT(*) > 1;

