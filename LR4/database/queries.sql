-- Запит 1: Студенти, народжені після 2000 року, відсортовані за прізвищем
SELECT first_name, last_name, birth_date, group_name
FROM students
WHERE birth_date >= '2000-01-01'
ORDER BY last_name ASC;

-- Запит 2: Студенти, які навчаються в групі 'КН-101', разом з курсами
SELECT
    s.first_name || ' ' || s.last_name AS student_name,
    c.course_name
FROM enrollments e
INNER JOIN students s ON e.student_id = s.student_id
INNER JOIN courses c ON e.course_id = c.course_id
WHERE s.group_name = 'КН-101';

-- Запит 3: Статистика по курсах (кількість студентів та середня оцінка)
SELECT
    c.course_name,
    COUNT(e.enrollment_id) AS student_count,
    AVG(e.grade) AS avg_grade
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name
HAVING COUNT(e.enrollment_id) > 0;

-- Запит 4: Студенти з оцінками вище середньої по всіх курсах
SELECT s.first_name || ' ' || s.last_name AS student_name, e.grade
FROM enrollments e
INNER JOIN students s ON e.student_id = s.student_id
WHERE e.grade > (SELECT AVG(grade) FROM enrollments)
ORDER BY e.grade DESC;

-- Запит 5: Детальна інформація по студентах та їх курсах
SELECT
    s.student_id,
    s.first_name || ' ' || s.last_name AS student_name,
    s.group_name,
    c.course_name,
    c.credits,
    e.grade
FROM enrollments e
INNER JOIN students s ON e.student_id = s.student_id
INNER JOIN courses c ON e.course_id = c.course_id
ORDER BY s.last_name, c.course_name;
