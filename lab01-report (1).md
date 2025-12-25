# Лабораторна робота 1. Робота з СУБД PostgreSQL та основи SQL

## Загальна інформація

**Здобувач освіти:** Вознюк Ілля
**Група:** ІПЗ-31
**Обраний рівень складності:** 1 та 2
**Посилання на проєкт:** https://cfwsviaxdhxudhrxqacx.supabase.co

## Виконання завдань

### Список таблиць

```sql
-- Запит для отримання списку таблиць
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
```

Результат: У базі даних створено 8 основних таблиць: categories, customers, employees, order_items, orders, products, regions, suppliers.

Скріншот

...


### 1.1 Отримати всі записи з таблиці customers.

```sql
SELECT * FROM customers;
```

Результат: Отримано 15 записів клієнтів, включаючи як фізичних осіб, так і юридичні особи з різних міст України.

Скріншот

[Продовжити для всіх завдань обраного рівня]


### 1.2 Вивести тільки назви товарів і їхні ціни з таблиці products.

```sql
SELECT product_name, 
        unit_price 
FROM products;
```

Результат: отримано тільки назви товарів і їхні ціни з таблиці products.

<img width="1352" height="495" alt="image" src="https://github.com/user-attachments/assets/270de16d-857d-48f9-b580-6dbee266b520" />



### 1.3 Показати контактні дані всіх співробітників (ім'я, прізвище, телефон, email).

```sql
SELECT first_name, 
        last_name,
        birth_date,
        email 
FROM employees;
```

Результат: отримано контактні дані всіх співробітників (ім'я, прізвище, телефон, email).

<img width="1359" height="493" alt="image" src="https://github.com/user-attachments/assets/05a6c575-adf5-41f1-b25b-7997a9920e5b" />


### 1.4 Знайти всіх клієнтів з міста Київ.


```sql
SELECT * FROM customers WHERE city LIKE 'Київ' ;
```

Результат: отримано всіх клієнтів з міста Київ.


<img width="1356" height="372" alt="image" src="https://github.com/user-attachments/assets/713a64a7-2fbf-4c30-bab3-05e2e14a4d64" />



### 1.5 Вивести товари, які коштують більше 25000 грн.

```sql
SELECT * FROM products WHERE unit_price > 25000 ;
```

Результат: отримано товари, які коштують більше 25000 грн.

<img width="612" height="513" alt="image" src="https://github.com/user-attachments/assets/5492843a-3ca8-465e-b93c-5d9ff21cddb8" />

### 1.6 Показати всі замовлення зі статусом 'delivered'.

```sql
SELECT * FROM orders WHERE order_status LIKE 'delivered' ;
```

Результат: отримано всі замовлення зі статусом 'delivered'.

<img width="631" height="512" alt="image" src="https://github.com/user-attachments/assets/90caebef-2e09-4ef6-83d4-f480c335fdb6" />



### 1.7 Знайти співробітників, які працюють у відділі продажів (посада містить слово "продаж").

```sql
SELECT * FROM employees WHERE title LIKE '%продажу' ;
```

Результат: отримано співробітників, які працюють у відділі продажів (посада містить слово "продаж").

<img width="621" height="468" alt="image" src="https://github.com/user-attachments/assets/018dc357-cbda-4bfb-af6f-0a48d9ed068e" />



### 1.8 Відсортувати товари за зростанням ціни.

```sql
SELECT * FROM products ORDER BY unit_price;
```

Результат: отримано відсортовані товари за зростанням ціни.

<img width="608" height="481" alt="image" src="https://github.com/user-attachments/assets/b21b5b2e-e9dc-4045-8def-df97bcbd0976" />



### 1.9 Показати клієнтів в алфавітному порядку за іменем контактної особи.

```sql
SELECT * FROM customers ORDER BY contact_name;
```

Результат: отримано клієнтів в алфавітному порядку за іменем контактної особи.

<img width="622" height="508" alt="image" src="https://github.com/user-attachments/assets/f4ba122d-d18c-4901-af32-93a480cc1126" />



### 1.10 Вивести замовлення від найновіших до найстаріших.

```sql
SELECT * FROM orders ORDER BY order_date DESC;
```

Результат: отримано замовлення від найновіших до найстаріших.

<img width="613" height="501" alt="image" src="https://github.com/user-attachments/assets/daea97f3-f3fb-4214-9340-5d9a202bcdd9" />



### 1.11 Показати перші 10 найдорожчих товарів.

```sql
SELECT * FROM products ORDER BY unit_price DESC LIMIT 10;
```

Результат: отримано перші 10 найдорожчих товарів.

<img width="621" height="483" alt="image" src="https://github.com/user-attachments/assets/ff2ada9c-8e23-47e3-8508-ea7a7280d137" />



### 1.12 Вивести 5 останніх замовлень (за датою).

```sql
SELECT * FROM orders ORDER BY order_date DESC LIMIT 5;
```

Результат: отримано 5 останніх замовлень (за датою).

<img width="619" height="424" alt="image" src="https://github.com/user-attachments/assets/07ca6376-d1af-4579-a181-9e69e4a3f889" />



### 1.13 Отримати перших 8 клієнтів в алфавітному порядку.

```sql
SELECT * FROM customers ORDER BY contact_name LIMIT 8;
```

Результат: отримано перших 8 клієнтів в алфавітному порядку.

<img width="601" height="501" alt="image" src="https://github.com/user-attachments/assets/90ac040c-11a4-4b76-b825-40260e8f2b07" />



#####################################################################

### 2.1 Знайти всіх клієнтів, чиї імена починаються на "Іван".

```sql
SELECT * FROM customers WHERE contact_name LIKE 'Іван%';
```

Результат: отримано всіх клієнтів, чиї імена починаються на "Іван".

<img width="602" height="476" alt="image" src="https://github.com/user-attachments/assets/80ac78bd-0cf1-4b11-b7b4-11c5e9f4b180" />



### 2.2 Вивести товари, в назві яких є слово "phone" або "телефон".

```sql
SELECT * FROM products 
WHERE product_name = 'phone' OR  product_name = 'телефон';
```

Результат: отримано товари, в назві яких є слово "phone" або "телефон".

<img width="618" height="507" alt="image" src="https://github.com/user-attachments/assets/7e85cb8c-2aab-4d9c-ae90-ddd3ce79900b" />



### 2.3 Самостійно: Придумати та виконати 3 власні запити з використанням LIKE для пошуку за різними зразками (початок, кінець, містить).


```sql
SELECT * FROM customers 
WHERE contact_name LIKE '%Ольга';

SELECT * FROM customers 
WHERE contact_name LIKE 'Ольга%';

SELECT * FROM customers 
WHERE contact_name LIKE '%Ольга%';
```

Результат: отримано 3 власні запити з використанням LIKE для пошуку за різними зразками (початок, кінець, містить).

<img width="621" height="512" alt="image" src="https://github.com/user-attachments/assets/5be8d11e-c475-4397-848e-69606bd2530b" />

<img width="624" height="508" alt="image" src="https://github.com/user-attachments/assets/812a0332-90bf-4a11-afad-0f05fbd37119" />

<img width="633" height="507" alt="image" src="https://github.com/user-attachments/assets/61b7b525-a0f5-45fe-8639-0e256fa497c2" />



### 2.4 Знайти товари дорожчі за 15000 грн і дешевші за 50000 грн.

```sql
SELECT * FROM products WHERE unit_price > 15000 AND unit_price < 50000 ;
```

Результат: отримано товари дорожчі за 15000 грн і дешевші за 50000 грн.

<img width="609" height="477" alt="image" src="https://github.com/user-attachments/assets/a4280ddd-022b-46a7-a72b-7043e5511a66" />



### 2.5 Вивести клієнтів з Києва або Львова, які є юридичними особами.

```sql
SELECT * FROM customers 
WHERE (city = 'Київ' OR city = 'Львів') 
AND company_name IS NOT NULL;
```

Результат: отримано клієнтів з Києва або Львова, які є юридичними особами.

<img width="616" height="515" alt="image" src="https://github.com/user-attachments/assets/2833c01e-4225-452a-8d84-a50141dcc7b2" />



### 2.6 Самостійно: Створити 4 власні запити з комбінаціями логічних операторів для різних таблиць.


### 1
```sql
SELECT * FROM products WHERE unit_price > 20000 AND unit_price < 35000 ;
```

<img width="639" height="527" alt="image" src="https://github.com/user-attachments/assets/12e960e0-d52a-4a92-8234-7a65dbc130ce" />


### 2

```sql
SELECT * FROM customers WHERE city LIKE 'Київ' OR city LIKE 'Харків' ;
```

<img width="610" height="476" alt="image" src="https://github.com/user-attachments/assets/d1a10ae3-b376-418e-8779-0f22092d7e66" />

### 3

```sql
SELECT * FROM regions
WHERE region_name LIKE '%область'
AND region_id IS NOT NULL;
```

<img width="611" height="486" alt="image" src="https://github.com/user-attachments/assets/fa17de8a-dabc-4179-b7de-773d4567a75a" />

### 4

```sql
SELECT * FROM suppliers
WHERE supplier_id < 5
AND company_name LIKE 'ТОВ%';
```

<img width="640" height="494" alt="image" src="https://github.com/user-attachments/assets/88587da5-af16-4447-a6a5-50d726aa3aa2" />


Результат: отримано 4 власні запити з комбінаціями логічних операторів для різних таблиць.


### 2.7 Вивести клієнтів з міст Київ, Харків, Одеса, Дніпро.

```sql
SELECT * FROM customers WHERE city IN ('Київ', 'Харків', 'Одеса', 'Дніпро')
```

Результат: отримано клієнтів з міст Київ, Харків, Одеса, Дніпро.

<img width="630" height="528" alt="image" src="https://github.com/user-attachments/assets/3855fd11-5590-46c3-a050-5141376d493d" />



###2.8 Знайти товари в ціновому діапазоні від 10000 до 30000 грн.

```sql
SELECT * FROM products WHERE unit_price BETWEEN 10000 AND 30000;
```

Результат: отримано товари в ціновому діапазоні від 10000 до 30000 грн.

<img width="585" height="500" alt="image" src="https://github.com/user-attachments/assets/92f6de68-8ed3-4760-8e8b-76326194b3f5" />



### 2.9 Придумати та виконати по 2 запити для кожного оператора (IN, BETWEEN, IS NULL/IS NOT NULL).

### 1

```sql
SELECT * FROM customers WHERE city IN('Харків', 'Одеса');В
```
<img width="603" height="508" alt="image" src="https://github.com/user-attachments/assets/71b7faca-7c9f-411c-8f60-98fae5e3dae6" />

### 2

```sql
SELECT * FROM suppliers WHERE contact_title IN('Директор', 'Менеджер', 'Власник');
```
<img width="611" height="491" alt="image" src="https://github.com/user-attachments/assets/83a51b21-86f6-4e2b-8e7c-68f22ea43852" />


### 3

```sql
SELECT * FROM products WHERE units_in_stock BETWEEN 10 AND 30;
```
<img width="623" height="473" alt="image" src="https://github.com/user-attachments/assets/b4a18730-4efa-4700-89ba-de4852025b23" />

### 4

```sql
SELECT * FROM products WHERE product_id BETWEEN 10 AND 20;
```
<img width="606" height="505" alt="image" src="https://github.com/user-attachments/assets/02c4a2fa-5da8-4f0d-8be9-be746a7c155d" />

### 5

```sql
SELECT * FROM customers WHERE company_name IS NOT NULL;
```
<img width="606" height="505" alt="image" src="https://github.com/user-attachments/assets/fac7611e-9f5f-4963-8550-bf59f93fcb93" />

### 6

```sql
SELECT * FROM customers WHERE company_name IS NULL;
```
<img width="632" height="503" alt="image" src="https://github.com/user-attachments/assets/d4e4655e-cdf1-4797-9521-d7df083303f2" />

Результат: отримано по 2 запити для кожного оператора (IN, BETWEEN, IS NULL/IS NOT NULL).



### 2.10 Створити 5 складних запитів, які поєднують різні типи умов (LIKE + AND/OR, BETWEEN + IN, тощо).

```sql
SELECT * FROM customers WHERE contact_name LIKE 'Іван%' AND customer_id <10;

SELECT * FROM customers WHERE contact_name LIKE 'Іван%' OR city LIKE 'Одеса';

SELECT * FROM customers
WHERE (contact_name LIKE 'Іван%' OR city LIKE 'Одеса')
AND customer_id = 6;

SELECT * FROM customers
WHERE city IN('Львів', 'Київ')
AND company_name IS NULL;

SELECT * FROM customers
WHERE region_id BETWEEN 3 AND 17
AND company_name IS NOT NULL;
```

<img width="611" height="469" alt="image" src="https://github.com/user-attachments/assets/20a31625-0413-4736-8314-1503a09d8610" />
<img width="621" height="456" alt="image" src="https://github.com/user-attachments/assets/a1393db7-ee93-45bb-970f-79d46550e94a" />
<img width="594" height="460" alt="image" src="https://github.com/user-attachments/assets/1087c809-214f-40ec-a9bd-ed1de3a362a7" />
<img width="636" height="479" alt="image" src="https://github.com/user-attachments/assets/7e29a03b-0545-4a6a-a93f-570b9a282c96" />
<img width="597" height="435" alt="image" src="https://github.com/user-attachments/assets/904747b7-eefb-43f9-888a-749a60018da9" />



Результат: отримано 5 складних запитів, які поєднують різні типи умов (LIKE + AND/OR, BETWEEN + IN, тощо).



### 2.11 Написати 3 запити з сортуванням за кількома полями та 2 запити з використанням OFFSET для пагінації.

```sql
SELECT * FROM customers ORDER BY contact_name;

SELECT * FROM customers ORDER BY address DESC;

SELECT * FROM customers ORDER BY customer_id DESC;
```

<img width="607" height="475" alt="image" src="https://github.com/user-attachments/assets/5f5be2e7-0fa6-4f17-9e1d-2120e75af196" />
<img width="622" height="535" alt="image" src="https://github.com/user-attachments/assets/3f85a30a-2317-43ec-9739-a5ac36d7eedf" />
<img width="609" height="414" alt="image" src="https://github.com/user-attachments/assets/d094cc27-ca72-4cdf-9c6e-cf4a257f5a8b" />


```sql
SELECT *
FROM orders
ORDER BY order_date DESC
LIMIT 5 OFFSET 0;
```

<img width="605" height="466" alt="image" src="https://github.com/user-attachments/assets/eb67771b-5f80-4ea9-ab51-dae27db453b9" />

```sql
SELECT *
FROM suppliers
ORDER BY postal_code DESC
LIMIT 15 OFFSET 0;
```

<img width="653" height="478" alt="image" src="https://github.com/user-attachments/assets/287c94bd-e53f-42a2-8f73-6f8061cf5e45" />



Результат: отримано 3 запити з сортуванням за кількома полями та 2 запити з використанням OFFSET для пагінації.


## Висновки

**Самооцінка**: Заслуговую на 4)

**Обгрунтування**: Я зробив завдання лише на 1 та 2 рівень що пітверджує оцінку не більше 4, розібрався у роботі легких та важких запитів та можу користуватись ними без стороньої допомоги, також старався дотримуватись вимог до оформлення читабельності коду та оформлення звіту і вважаю що відповідаю вимогам для отримання такого балу
