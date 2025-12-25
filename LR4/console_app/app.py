from flask import Flask, render_template, request, redirect, url_for, flash
from database import DatabaseConnection

app = Flask(__name__)
app.secret_key = 'bkKJF8fSDjb532Bjkbhvf97Afhm15khbfd&k'

# Підключення до бази даних
db = DatabaseConnection(
    dbname='stud',  # змінили з 'student_courses' на 'stud'
    user='postgres',
    password='password',
    host='127.20.0.2',
    port=5432
)
db.connect()

# ---------------- Головна сторінка ----------------
@app.route('/')
def index():
    return render_template('index.html')

# ---------------- Студенти ----------------
@app.route('/students')
def students():
    query = "SELECT student_id, full_name, group_name, birth_date FROM students ORDER BY full_name"
    cursor = db.execute_query(query)
    students_list = cursor.fetchall() if cursor else []
    return render_template('stud.html', students=students_list)

@app.route('/students/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        full_name = request.form['full_name']
        group_name = request.form['group_name']
        birth_date = request.form['birth_date']

        query = """
            INSERT INTO students (full_name, group_name, birth_date)
            VALUES (%s, %s, %s)
        """
        cursor = db.execute_query(query, (full_name, group_name, birth_date))
        if cursor:
            flash('Студента успішно додано!', 'success')
            return redirect(url_for('students'))
        else:
            flash('Помилка додавання студента', 'error')

    return render_template('add_stud.html')

@app.route('/students/edit/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    if request.method == 'POST':
        full_name = request.form['full_name']
        group_name = request.form['group_name']
        birth_date = request.form['birth_date']

        query = """
            UPDATE students
            SET full_name = %s, group_name = %s, birth_date = %s
            WHERE student_id = %s
        """
        cursor = db.execute_query(query, (full_name, group_name, birth_date, student_id))
        if cursor:
            flash('Дані студента успішно оновлено!', 'success')
            return redirect(url_for('students'))
        else:
            flash('Помилка оновлення студента', 'error')

    query = "SELECT * FROM students WHERE student_id = %s"
    cursor = db.execute_query(query, (student_id,))
    student = cursor.fetchone() if cursor else None
    return render_template('edit_stud.html', student=student)

@app.route('/students/delete/<int:student_id>')
def delete_student(student_id):
    query = "DELETE FROM students WHERE student_id = %s"
    cursor = db.execute_query(query, (student_id,))
    if cursor:
        flash('Студента видалено!', 'success')
    else:
        flash('Помилка видалення студента', 'error')
    return redirect(url_for('students'))

# ---------------- Курси ----------------
@app.route('/courses')
def courses():
    query = "SELECT course_id, course_name, description, credits FROM courses ORDER BY course_name"
    cursor = db.execute_query(query)
    courses_list = cursor.fetchall() if cursor else []
    return render_template('courses.html', courses=courses_list)

@app.route('/courses/add', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        course_name = request.form['course_name']
        description = request.form['description']
        credits = int(request.form['credits'])

        query = """
            INSERT INTO courses (course_name, description, credits)
            VALUES (%s, %s, %s)
        """
        cursor = db.execute_query(query, (course_name, description, credits))
        if cursor:
            flash('Курс успішно додано!', 'success')
            return redirect(url_for('courses'))
        else:
            flash('Помилка додавання курсу', 'error')

    return render_template('add_course.html')

@app.route('/courses/delete/<int:course_id>')
def delete_course(course_id):
    query = "DELETE FROM courses WHERE course_id = %s"
    cursor = db.execute_query(query, (course_id,))
    if cursor:
        flash('Курс видалено!', 'success')
    else:
        flash('Помилка видалення курсу', 'error')
    return redirect(url_for('courses'))

# ---------------- Зарахування ----------------
@app.route('/enrollments')
def enrollments():
    query = """
        SELECT e.enrollment_id, s.full_name, s.group_name, c.course_name, e.grade
        FROM enrollments e
        JOIN students s ON e.student_id = s.student_id
        JOIN courses c ON e.course_id = c.course_id
        ORDER BY s.full_name
    """
    cursor = db.execute_query(query)
    enrollments_list = cursor.fetchall() if cursor else []
    return render_template('enrollments.html', enrollments=enrollments_list)

@app.route('/enrollments/add', methods=['GET', 'POST'])
def add_enrollment():
    students_query = "SELECT student_id, full_name FROM students ORDER BY full_name"
    courses_query = "SELECT course_id, course_name FROM courses ORDER BY course_name"

    students_cursor = db.execute_query(students_query)
    courses_cursor = db.execute_query(courses_query)

    students_list = students_cursor.fetchall() if students_cursor else []
    courses_list = courses_cursor.fetchall() if courses_cursor else []

    if request.method == 'POST':
        student_id = int(request.form['student_id'])
        course_id = int(request.form['course_id'])
        grade_input = request.form.get('grade')
        grade = int(grade_input) if grade_input else None

        query = "INSERT INTO enrollments (student_id, course_id, grade) VALUES (%s, %s, %s)"
        cursor = db.execute_query(query, (student_id, course_id, grade))
        if cursor:
            flash('Студента зараховано на курс!', 'success')
            return redirect(url_for('enrollments'))
        else:
            flash('Помилка зарахування', 'error')

    return render_template('add_enrollment.html', students=students_list, courses=courses_list)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
