# Звіт з лабораторної роботи 5. Керування БД, оптимізація продуктивності та автоматизація

**Вознюк Ілля**
**Група: ІПЗ-31**
**Дата виконання:** 13 грудня 2025 року
**Варіант:** 1

## Мета роботи

Навчитися аналізувати та оптимізувати продуктивність баз даних через створення індексів та аналіз планів виконання запитів, опанувати механізми автоматизації за допомогою тригерів та представлень, освоїти базові операції адміністрування СУБД, включаючи керування правами доступу та резервне копіювання.

## Виконання роботи

### Рівень 1. 


#### Крок 2. Аналіз продуктивності запитів



**Список студентів з курсами та оцінками:**

```sql
EXPLAIN ANALYZE
SELECT 
    s.first_name,
	s.last_name,
    s.group_name,
    c.course_name,
    e.grade
FROM enrollments e
JOIN students s ON e.student_id = s.student_id
JOIN courses c ON e.course_id = c.course_id
ORDER BY s.first_name;
```

**Результат перевірки:**
```
"QUERY PLAN"
"Sort  (cost=148.68..152.60 rows=1570 width=524) (actual time=0.794..0.797 rows=5 loops=1)"
"  Sort Key: s.first_name"
"  Sort Method: quicksort  Memory: 25kB"
"  ->  Hash Join  (cost=31.25..65.34 rows=1570 width=524) (actual time=0.022..0.025 rows=5 loops=1)"
"        Hash Cond: (e.course_id = c.course_id)"
"        ->  Hash Join  (cost=15.18..45.07 rows=1570 width=310) (actual time=0.009..0.012 rows=5 loops=1)"
"              Hash Cond: (e.student_id = s.student_id)"
"              ->  Seq Scan on enrollments e  (cost=0.00..25.70 rows=1570 width=20) (actual time=0.002..0.002 rows=5 loops=1)"
"              ->  Hash  (cost=12.30..12.30 rows=230 width=298) (actual time=0.004..0.004 rows=3 loops=1)"
"                    Buckets: 1024  Batches: 1  Memory Usage: 9kB"
"                    ->  Seq Scan on students s  (cost=0.00..12.30 rows=230 width=298) (actual time=0.002..0.002 rows=3 loops=1)"
"        ->  Hash  (cost=12.70..12.70 rows=270 width=222) (actual time=0.009..0.009 rows=4 loops=1)"
"              Buckets: 1024  Batches: 1  Memory Usage: 9kB"
"              ->  Seq Scan on courses c  (cost=0.00..12.70 rows=270 width=222) (actual time=0.006..0.006 rows=4 loops=1)"
"Planning Time: 0.221 ms"
"Execution Time: 0.817 ms"
```


<img width="1501" height="924" alt="image" src="https://github.com/user-attachments/assets/3c72751b-9673-4614-96b8-9c70aa5dd52e" />


**Кількість студентів на кожному курсі:**

```sql
-- Приклад аналізу запиту
EXPLAIN ANALYZE
SELECT
    u.username,
    COUNT(o.order_id) as order_count,
    SUM(o.total_amount) as total_spent
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
WHERE u.created_at > '2024-01-01'
GROUP BY u.user_id, u.username
HAVING COUNT(o.order_id) > 5
ORDER BY total_spent DESC;
```

**Результат перевірки:**

```
"QUERY PLAN"
"Sort  (cost=63.46..63.96 rows=200 width=226) (actual time=0.203..0.205 rows=4 loops=1)"
"  Sort Key: (count(e.student_id)) DESC"
"  Sort Method: quicksort  Memory: 25kB"
"  ->  HashAggregate  (cost=53.81..55.81 rows=200 width=226) (actual time=0.194..0.196 rows=4 loops=1)"
"        Group Key: c.course_name"
"        Batches: 1  Memory Usage: 40kB"
"        ->  Hash Right Join  (cost=16.07..45.96 rows=1570 width=222) (actual time=0.186..0.189 rows=6 loops=1)"
"              Hash Cond: (e.course_id = c.course_id)"
"              ->  Seq Scan on enrollments e  (cost=0.00..25.70 rows=1570 width=8) (actual time=0.170..0.171 rows=5 loops=1)"
"              ->  Hash  (cost=12.70..12.70 rows=270 width=222) (actual time=0.009..0.010 rows=4 loops=1)"
"                    Buckets: 1024  Batches: 1  Memory Usage: 9kB"
"                    ->  Seq Scan on courses c  (cost=0.00..12.70 rows=270 width=222) (actual time=0.007..0.007 rows=4 loops=1)"
"Planning Time: 0.994 ms"
"Execution Time: 0.234 ms"
```

<img width="1401" height="873" alt="image" src="https://github.com/user-attachments/assets/246d7314-a7e1-4b98-a787-33a78ea1c997" />





**Студенти із середнім балом вище середнього по базі:**

```sql
EXPLAIN ANALYZE
SELECT 
    s.first_name,
    AVG(e.grade) AS avg_grade
FROM students s
JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name
HAVING AVG(e.grade) > (
    SELECT AVG(grade)
    FROM enrollments
    WHERE grade IS NOT NULL
);
```

**Результат перевірки:**
```
"QUERY PLAN"
"HashAggregate  (cost=82.54..85.99 rows=77 width=154) (actual time=0.048..0.052 rows=2 loops=1)"
"  Group Key: s.student_id"
"  Filter: (avg(e.grade) > $0)"
"  Batches: 1  Memory Usage: 40kB"
"  Rows Removed by Filter: 1"
"  InitPlan 1 (returns $0)"
"    ->  Aggregate  (cost=29.61..29.62 rows=1 width=32) (actual time=0.005..0.006 rows=1 loops=1)"
"          ->  Seq Scan on enrollments  (cost=0.00..25.70 rows=1562 width=12) (actual time=0.002..0.003 rows=5 loops=1)"
"                Filter: (grade IS NOT NULL)"
"  ->  Hash Join  (cost=15.18..45.07 rows=1570 width=134) (actual time=0.019..0.022 rows=5 loops=1)"
"        Hash Cond: (e.student_id = s.student_id)"
"        ->  Seq Scan on enrollments e  (cost=0.00..25.70 rows=1570 width=16) (actual time=0.006..0.006 rows=5 loops=1)"
"        ->  Hash  (cost=12.30..12.30 rows=230 width=122) (actual time=0.008..0.008 rows=3 loops=1)"
"              Buckets: 1024  Batches: 1  Memory Usage: 9kB"
"              ->  Seq Scan on students s  (cost=0.00..12.30 rows=230 width=122) (actual time=0.005..0.005 rows=3 loops=1)"
"Planning Time: 0.224 ms"
"Execution Time: 0.093 ms"
```

<img width="1505" height="892" alt="image" src="https://github.com/user-attachments/assets/d04fd336-dd45-437d-a233-5ca57ead5fa0" />




#### Крок 3. Створення індексів для оптимізації


**1. Індекси для JOIN:**

```sql
CREATE INDEX idx_enrollments_student_id
ON enrollments(student_id);

CREATE INDEX idx_enrollments_course_id
ON enrollments(course_id);
```


**2. Складений індекс для ORDER BY:**

```sql
CREATE INDEX idx_students_last_first_name
ON students(last_name, first_name);
```


**3. Індекс для агрегатних запитів:**

```sql
CREATE INDEX idx_enrollments_grade
ON enrollments(grade);
```


**Результат перевірки:**
```
"QUERY PLAN"
"Sort  (cost=2.18..2.19 rows=1 width=312) (actual time=0.033..0.034 rows=0 loops=1)"
"  Sort Key: (avg(e.grade)) DESC"
"  Sort Method: quicksort  Memory: 25kB"
"  ->  GroupAggregate  (cost=2.13..2.17 rows=1 width=312) (actual time=0.030..0.031 rows=0 loops=1)"
"        Group Key: s.student_id"
"        Filter: (count(e.enrollment_id) > 2)"
"        Rows Removed by Filter: 2"
"        ->  Sort  (cost=2.13..2.14 rows=2 width=256) (actual time=0.022..0.023 rows=3 loops=1)"
"              Sort Key: s.student_id"
"              Sort Method: quicksort  Memory: 25kB"
"              ->  Hash Right Join  (cost=1.05..2.12 rows=2 width=256) (actual time=0.016..0.019 rows=3 loops=1)"
"                    Hash Cond: (e.student_id = s.student_id)"
"                    ->  Seq Scan on enrollments e  (cost=0.00..1.05 rows=5 width=20) (actual time=0.003..0.004 rows=5 loops=1)"
"                    ->  Hash  (cost=1.04..1.04 rows=1 width=240) (actual time=0.009..0.009 rows=2 loops=1)"
"                          Buckets: 1024  Batches: 1  Memory Usage: 9kB"
"                          ->  Seq Scan on students s  (cost=0.00..1.04 rows=1 width=240) (actual time=0.006..0.006 rows=2 loops=1)"
"                                Filter: (birth_date > '2000-01-01'::date)"
"                                Rows Removed by Filter: 1"
"Planning Time: 0.137 ms"
"Execution Time: 0.058 ms"
```
<img width="1523" height="967" alt="image" src="https://github.com/user-attachments/assets/87365641-9aa1-41c7-a821-f8360f016102" />
```
"QUERY PLAN"
"Sort  (cost=16.17..16.19 rows=5 width=524) (actual time=0.048..0.050 rows=5 loops=1)"
"  Sort Key: s.first_name"
"  Sort Method: quicksort  Memory: 25kB"
"  ->  Nested Loop  (cost=1.11..16.12 rows=5 width=524) (actual time=0.032..0.038 rows=5 loops=1)"
"        Join Filter: (e.student_id = s.student_id)"
"        Rows Removed by Join Filter: 4"
"        ->  Hash Join  (cost=1.11..14.88 rows=5 width=234) (actual time=0.025..0.028 rows=5 loops=1)"
"              Hash Cond: (c.course_id = e.course_id)"
"              ->  Seq Scan on courses c  (cost=0.00..12.70 rows=270 width=222) (actual time=0.010..0.011 rows=4 loops=1)"
"              ->  Hash  (cost=1.05..1.05 rows=5 width=20) (actual time=0.009..0.010 rows=5 loops=1)"
"                    Buckets: 1024  Batches: 1  Memory Usage: 9kB"
"                    ->  Seq Scan on enrollments e  (cost=0.00..1.05 rows=5 width=20) (actual time=0.005..0.006 rows=5 loops=1)"
"        ->  Materialize  (cost=0.00..1.04 rows=3 width=298) (actual time=0.001..0.001 rows=2 loops=5)"
"              ->  Seq Scan on students s  (cost=0.00..1.03 rows=3 width=298) (actual time=0.003..0.004 rows=3 loops=1)"
"Planning Time: 0.214 ms"
"Execution Time: 0.074 ms"
```
<img width="1505" height="965" alt="image" src="https://github.com/user-attachments/assets/e4f693d0-354f-45d3-85e3-3a9c493672dc" />
```
"QUERY PLAN"
"HashAggregate  (cost=3.24..3.29 rows=1 width=154) (actual time=0.034..0.038 rows=2 loops=1)"
"  Group Key: s.student_id"
"  Filter: (avg(e.grade) > $0)"
"  Batches: 1  Memory Usage: 24kB"
"  Rows Removed by Filter: 1"
"  InitPlan 1 (returns $0)"
"    ->  Aggregate  (cost=1.06..1.07 rows=1 width=32) (actual time=0.004..0.004 rows=1 loops=1)"
"          ->  Seq Scan on enrollments  (cost=0.00..1.05 rows=5 width=12) (actual time=0.001..0.002 rows=5 loops=1)"
"                Filter: (grade IS NOT NULL)"
"  ->  Hash Join  (cost=1.07..2.14 rows=5 width=134) (actual time=0.020..0.022 rows=5 loops=1)"
"        Hash Cond: (e.student_id = s.student_id)"
"        ->  Seq Scan on enrollments e  (cost=0.00..1.05 rows=5 width=16) (actual time=0.007..0.007 rows=5 loops=1)"
"        ->  Hash  (cost=1.03..1.03 rows=3 width=122) (actual time=0.008..0.008 rows=3 loops=1)"
"              Buckets: 1024  Batches: 1  Memory Usage: 9kB"
"              ->  Seq Scan on students s  (cost=0.00..1.03 rows=3 width=122) (actual time=0.005..0.005 rows=3 loops=1)"
"Planning Time: 0.221 ms"
"Execution Time: 0.079 ms"
```
<img width="1507" height="972" alt="image" src="https://github.com/user-attachments/assets/f12687f2-c733-4366-8a32-fbb88c9ec0d8" />


Загальна таблиця порівняння
Запит	            До індексів (ms)	Після індексів     (ms)	Покращення
JOIN + ORDER BY	    0.817	            0.074	            ~91%
GROUP BY	        0.234	            0.058	            ~75%
HAVING + AVG	    0.093	            0.079	            ~15%



#### Крок 4. Створення представлень


**Просте представлення для активних користувачів:**

```sql
CREATE VIEW students_basic_info AS
SELECT
    student_id,
    first_name,
    last_name,
    group_name,
    birth_date
FROM students;
```
**Результат перевірки:**
```
SELECT * FROM students LIMIT 3;
```
<img width="1505" height="908" alt="image" src="https://github.com/user-attachments/assets/f3d499d7-5255-4be0-bbb5-d674d45a69e9" />


**Складне представлення з агрегацією:**
```sql
CREATE VIEW student_statistics AS
SELECT
    s.student_id,
    s.first_name,
    s.last_name,
    COUNT(e.course_id) AS total_courses,
    ROUND(AVG(e.grade), 2) AS avg_grade,
    MAX(e.grade) AS max_grade
FROM students s
LEFT JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name;

```
**Результат перевірки:**
```
SELECT *
FROM student_statistics
ORDER BY avg_grade DESC
LIMIT 10;

```
<img width="1474" height="912" alt="image" src="https://github.com/user-attachments/assets/9cd6cea8-24aa-4da0-990c-a1528864122d" />


#### Крок 5. Реалізація тригерів

```sql
--Створення таблиці для логування операцій
CREATE TABLE IF NOT EXISTS audit_log (
    log_id SERIAL PRIMARY KEY,
    table_name VARCHAR(50) NOT NULL,
    operation VARCHAR(10) NOT NULL,
    record_id INTEGER,
    old_values JSONB,
    new_values JSONB,
    changed_by VARCHAR(100),
    changed_at TIMESTAMP DEFAULT NOW()
);
```

```sql
--Функція для логування INSERT та UPDATE
CREATE OR REPLACE FUNCTION log_student_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (table_name, operation, record_id, new_values, changed_by)
        VALUES ('students', TG_OP, NEW.student_id, row_to_json(NEW)::jsonb, current_user);
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (table_name, operation, record_id, old_values, new_values, changed_by)
        VALUES ('students', TG_OP, NEW.student_id, row_to_json(OLD)::jsonb, row_to_json(NEW)::jsonb, current_user);
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;
```

```sql
--Тригери для логування
-- Логування вставки
CREATE TRIGGER trg_student_insert
AFTER INSERT ON students
FOR EACH ROW
EXECUTE FUNCTION log_student_changes();

-- Логування оновлення
CREATE TRIGGER trg_student_update
AFTER UPDATE ON students
FOR EACH ROW
EXECUTE FUNCTION log_student_changes();
```

```sql
--Функція для валідації email (якщо є стовпець email)
CREATE OR REPLACE FUNCTION validate_student_email()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.email IS NOT NULL AND NEW.email !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' THEN
        RAISE EXCEPTION 'Invalid email format: %', NEW.email;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

Тригер валідації
CREATE TRIGGER trg_validate_student_email
BEFORE INSERT OR UPDATE ON students
FOR EACH ROW
EXECUTE FUNCTION validate_student_email();
```



**Результат вставки:**
```sql
-- Вставка
INSERT INTO students (first_name, last_name, group_name, birth_date)
VALUES ('Ivan', 'Petrenko', 'CS-101', '2002-05-10');

-- Оновлення
UPDATE students
SET group_name = 'CS-102'
WHERE first_name='Ivan' AND last_name='Petrenko';

-- Перевірка логів
SELECT * FROM audit_log ORDER BY changed_at DESC LIMIT 5;
```


<img width="1507" height="928" alt="image" src="https://github.com/user-attachments/assets/847c0255-6fcf-4788-8720-38eb0b9beb19" />



#### Крок 6. Безпечне видалення


**Створення користувача з обмеженими правами:**
```sql
-- Створення користувача
CREATE USER report_viewer WITH PASSWORD 'secure_password';
```

**Надання базових прав:**
```sql
-- Підключення до бази
GRANT CONNECT ON DATABASE stud TO report_viewer;

-- Доступ до схеми
GRANT USAGE ON SCHEMA public TO report_viewer;
```

**Надання прав тільки на читання таблиць:**
```sql
-- Читання з таблиць
GRANT SELECT ON students, courses, enrollments TO report_viewer;
```

**Надання доступу до представлень (якщо вони створені):**
```sql
-- Якщо ти створив представлення student_statistics або active_students
GRANT SELECT ON student_statistics TO report_viewer;
GRANT SELECT ON active_students TO report_viewer;
```


```
-- Спроба вставки (заборонено)
INSERT INTO students (first_name, last_name, group_name, birth_date)
VALUES ('Test', 'User', 'CS-999', '2000-01-01');

-- Спроба оновлення (заборонено)
UPDATE students SET group_name='CS-102' WHERE student_id=1;

-- Спроба видалення (заборонено)
DELETE FROM students WHERE student_id=1;
Якщо права налаштовані правильно, отримаєш помилку типу:


ERROR:  permission denied for table students
```




#### Крок 7. Додавання нових таблиць

**Резервне копіювання**

**Повне копіювання у форматі дампу:**
```
pg_dump -U postgres -d stud -F c -f backup_$(date +%Y%m%d).dump
```

**Копіювання у SQL формат:**
```
pg_dump -U postgres -d stud > backup_stud.sql
```

**Відновлення у тестову базу**

**Створення тестової бази:**
```
createdb -U postgres test_restore
```

**Відновлення з дампу:**
```
pg_restore -U postgres -d test_restore backup_*.dump
```

**Відновлення з SQL файлу:**
```
psql -U postgres -d test_restore -f backup_stud.sql
```





## Висновки

У цій лабораторній роботі я опрацював ключові аспекти оптимізації та адміністрування баз даних PostgreSQL:
Використання EXPLAIN та EXPLAIN ANALYZE дозволяє оцінювати план виконання запитів та фактичну продуктивність.
Індекси суттєво прискорюють пошук та сортування, але надмірна кількість індексів уповільнює вставку та оновлення даних. Часткові та складені індекси дають ефективний компроміс для великих таблиць.
Представлення (VIEW) спрощують доступ до даних, а матеріалізовані представлення підвищують швидкість для складних агрегатних запитів.
Тригери та логування допомагають контролювати зміни в базі та забезпечують цілісність даних.
Правильне управління користувачами та правами доступу підвищує безпеку бази.
Резервне копіювання та PITR забезпечують відновлення даних у разі збою, а робота з базами через дампи SQL або фізичні файли дозволяє вибирати оптимальний метод відновлення.
Загалом, поєднання індексів, представлень, тригерів і правильного адміністрування прав користувачів дозволяє створити продуктивну, безпечну та керовану базу даних.







    Різниця між EXPLAIN та EXPLAIN ANALYZE
EXPLAIN – показує план виконання запиту, тобто як PostgreSQL планує виконати запит (послідовність сканувань, джоінів, сортування).
Не виконує сам запит.
Використовується для аналізу структури запиту та оптимізації без реальних витрат часу.
EXPLAIN ANALYZE – виконує запит і показує реальний час виконання кожного кроку разом із планом.
Використовується для оцінки продуктивності запиту на реальних даних.
Висновок:
EXPLAIN – коли хочеш оцінити план, не виконуючи дані.
EXPLAIN ANALYZE – коли потрібно реально заміряти час і ефективність.

    Типи індексів у PostgreSQL
B-Tree – стандартний індекс, підходить для:
пошуку за =, <, >, BETWEEN;
ORDER BY;
Найчастіше використовується.
Hash – для швидкого точного пошуку (=).
Не підтримує діапазони та сортування.
GIN (Generalized Inverted Index) – для колонок типу jsonb, tsvector.
Оптимізує пошук по складних структурах (наприклад, повнотекстовий пошук).
GiST (Generalized Search Tree) – для геометричних типів та пошуку за відстанню.
SP-GiST – спеціальні просторові структури, наприклад для quadtrees.
BRIN (Block Range INdex) – для дуже великих таблиць з послідовними значеннями (дати, ID).
Використовується для швидкого відсіювання діапазонів.

    Часткові індекси
Що це: індекс не на всю таблицю, а тільки на рядки, що відповідають умові WHERE.
Приклад:
CREATE INDEX idx_active_students ON students(last_name) WHERE is_active = TRUE;

    Звичайне VIEW vs MATERIALIZED VIEW
Критерій	VIEW	MATERIALIZED VIEW
Зберігання даних	Не зберігає, дані беруться при виконанні	Зберігає результат фізично
Оновлення	Кожен SELECT звертається до таблиць	Потрібне ручне REFRESH MATERIALIZED VIEW
Використання	Динамічні дані	Швидкий доступ до складних обчислень
Приклад	Перегляд активних студентів	Звіт із сумарними оцінками студентів

    Життєвий цикл тригера
BEFORE – виконується до операції (INSERT/UPDATE/DELETE).
Можна змінити або відхилити дані.
AFTER – виконується після операції.
Для логування, синхронізації, сповіщень.
INSTEAD OF – використовується на VIEW для заміни стандартної операції.
Наприклад, дозволяє вставляти дані у VIEW, який агрегує таблиці.

    Обмеження прав доступу
Важливо: щоб користувачі не могли випадково або зловмисно змінювати дані.
Гранулярність у PostgreSQL:
DATABASE – підключення до бази;
SCHEMA – доступ до схем;
TABLE / VIEW – SELECT, INSERT, UPDATE, DELETE;
COLUMN – доступ до окремих колонок;
FUNCTION – виконання функцій/триггерів.

    Логічне vs Фізичне резервне копіювання
Фізичне: копіюються всі файли бази.
Швидке відновлення, точна копія.
Не читається SQL.
Логічне: дамп SQL (pg_dump).
Можна переносити на інші версії або структури.
Повільніше на великих базах.

    Каскадні тригери
Що це: тригери, що викликають інші тригери після зміни таблиці.
Приклад:
Видаляємо курс → каскадно видаляються зарахування → каскадно логуються зміни.

    Вплив індексів на INSERT/UPDATE/DELETE
Індекси прискорюють SELECT, але уповільнюють зміни даних.
Чому: після вставки/оновлення/видалення потрібно оновлювати всі індекси.
Надмірна індексація:
Більше часу на модифікації;
Зайва пам’ять;
Може уповільнити загальну продуктивність.

    Point-in-time recovery (PITR)

Мета: відновити базу у точний момент часу після збою.
Компоненти PostgreSQL:
Резервна копія бази (base backup)
Write-Ahead Logs (WAL) – журнал транзакцій
Стратегія:
Створюємо base backup.
Збираємо WAL файли.
Відновлюємо базу і "прокручуємо" WAL до потрібного моменту.
