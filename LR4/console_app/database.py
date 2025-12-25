import psycopg2
from psycopg2 import sql

class DatabaseConnection:
    def __init__(self, dbname='stud', user='postgres',
                 password='password', host='127.20.0.2', port=5432):
        """
        dbname: назва твоєї БД
        user: користувач PostgreSQL
        password: пароль користувача
        host: хост (localhost зазвичай)
        port: порт (за замовчуванням 5432)
        """
        self.conn_params = {
            'dbname': 'stud',
            'user': 'postgres',
            'password': 'password',
            'host': '127.20.0.2',
            'port': 5432
        }
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            print("Успішне підключення до бази даних")
        except Exception as e:
            print(f"Помилка підключення: {e}")

    def disconnect(self):
        if self.conn:
            self.conn.close()
            print("З'єднання закрито")

    def execute_query(self, query, params=None, fetch=False):
        """
        Виконання будь-якого SQL-запиту.
        fetch=True повертає результати SELECT.
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
                if fetch:
                    result = cursor.fetchall()
                    return result
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"Помилка виконання запиту: {e}")
            return None

# Приклад використання:

if __name__ == "__main__":
    db = DatabaseConnection(dbname="student_courses", user="postgres", password="твій_пароль")
    db.connect()
    
    # Приклад: отримати всіх студентів
    students = db.execute_query("SELECT * FROM students", fetch=True)
    for s in students:
        print(s)
    
    db.disconnect()
