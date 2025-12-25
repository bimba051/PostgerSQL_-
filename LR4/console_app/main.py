from database import DatabaseConnection

# ---------------- CRUD для студентів ----------------
def add_student(db, full_name, group_name, birth_date):
    query = """
        INSERT INTO students (full_name, group_name, birth_date)
        VALUES (%s, %s, %s)
        RETURNING student_id
    """
    cursor = db.execute_query(query, (full_name, group_name, birth_date))
    if cursor:
        student_id = cursor.fetchone()[0]
        print(f"Студента додано з ID: {student_id}")
        return student_id
    return None

def get_all_students(db):
    query = "SELECT student_id, full_name, group_name, birth_date FROM students ORDER BY full_name"
    return db.execute_query(query, fetch=True)

# ---------------- CRUD для курсів ----------------
def add_course(db, course_name, description, credits):
    query = """
        INSERT INTO courses (course_name, description, credits)
        VALUES (%s, %s, %s)
        RETURNING course_id
    """
    cursor = db.execute_query(query, (course_name, description, credits))
    if cursor:
        course_id = cursor.fetchone()[0]
        print(f"Курс додано з ID: {course_id}")
        return course_id
    return None

def get_all_courses(db):
    query = "SELECT course_id, course_name, description, credits FROM courses ORDER BY course_name"
    return db.execute_query(query, fetch=True)

# ---------------- CRUD для записів на курси ----------------
def enroll_student(db, student_id, course_id, grade=None):
    query = """
        INSERT INTO enrollments (student_id, course_id, grade)
        VALUES (%s, %s, %s)
        RETURNING enrollment_id
    """
    cursor = db.execute_query(query, (student_id, course_id, grade))
    if cursor:
        enrollment_id = cursor.fetchone()[0]
        print(f"Студента зараховано на курс, запис ID: {enrollment_id}")
        return enrollment_id
    return None

def get_enrollments(db):
    query = """
        SELECT e.enrollment_id, s.full_name, s.group_name, c.course_name, e.grade
        FROM enrollments e
        JOIN students s ON e.student_id = s.student_id
        JOIN courses c ON e.course_id = c.course_id
        ORDER BY s.full_name
    """
    return db.execute_query(query, fetch=True)

# ---------------- Вивід ----------------
def display_students(students):
    print("\n" + "-"*70)
    print(f"{'ID':<5} {'Студент':<25} {'Група':<10} {'Дата народження':<15}")
    print("-"*70)
    for s in students:
        print(f"{s[0]:<5} {s[1]:<25} {s[2]:<10} {s[3]:<15}")
    print("-"*70)

def display_courses(courses):
    print("\n" + "-"*70)
    print(f"{'ID':<5} {'Назва курсу':<25} {'Опис':<25} {'Кредити':<8}")
    print("-"*70)
    for c in courses:
        print(f"{c[0]:<5} {c[1]:<25} {c[2]:<25} {c[3]:<8}")
    print("-"*70)

def display_enrollments(enrollments):
    print("\n" + "-"*90)
    print(f"{'ID':<5} {'Студент':<25} {'Група':<10} {'Курс':<30} {'Оцінка':<8}")
    print("-"*90)
    for e in enrollments:
        print(f"{e[0]:<5} {e[1]:<25} {e[2]:<10} {e[3]:<30} {str(e[4]):<8}")
    print("-"*90)

# ---------------- Меню ----------------
def main_menu():
    print("\n" + "="*50)
    print("СИСТЕМА УПРАВЛІННЯ СТУДЕНТАМИ ТА КУРСАМИ")
    print("="*50)
    print("1. Переглянути всіх студентів")
    print("2. Переглянути всі курси")
    print("3. Додати студента")
    print("4. Додати курс")
    print("5. Зарахувати студента на курс")
    print("6. Переглянути зарахування студентів")
    print("0. Вихід")
    print("="*50)
    return input("Оберіть опцію: ")

# ---------------- Головна функція ----------------
def main():
    db = DatabaseConnection(dbname="student_courses", user="postgres", password="твій_пароль")
    db.connect()

    if not db.conn:
        print("Не вдалося підключитися до бази даних")
        return

    while True:
        choice = main_menu()

        if choice == '1':
            students = get_all_students(db)
            display_students(students)

        elif choice == '2':
            courses = get_all_courses(db)
            display_courses(courses)

        elif choice == '3':
            full_name = input("ПІБ студента: ")
            group_name = input("Група: ")
            birth_date = input("Дата народження (YYYY-MM-DD): ")
            add_student(db, full_name, group_name, birth_date)

        elif choice == '4':
            course_name = input("Назва курсу: ")
            description = input("Опис: ")
            credits = int(input("Кредити: "))
            add_course(db, course_name, description, credits)

        elif choice == '5':
            students = get_all_students(db)
            display_students(students)
            student_id = int(input("ID студента: "))

            courses = get_all_courses(db)
            display_courses(courses)
            course_id = int(input("ID курсу: "))

            grade_input = input("Оцінка (не обов'язково): ")
            grade = int(grade_input) if grade_input else None
            enroll_student(db, student_id, course_id, grade)

        elif choice == '6':
            enrollments = get_enrollments(db)
            display_enrollments(enrollments)

        elif choice == '0':
            print("Дякуємо за використання системи!")
            break

        else:
            print("Невірна опція! Спробуйте ще раз.")

        input("Натисніть Enter для продовження...")

    db.disconnect()

if __name__ == "__main__":
    main()
