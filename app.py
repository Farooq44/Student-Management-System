from flask import Flask, render_template, request, redirect, url_for
import mysql.connector as mysql_connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


#connect to MySQL
db = mysql_connector.connect(
    host = os.getenv('DB_HOST'),
    port=int(os.getenv("DB_PORT")),
    user = os.getenv('DB_USER'),
    password = os.getenv('DB_PASSWORD'),
    database = os.getenv("DB_NAME")
)

cursor = db.cursor()

#Home Route - Display all Students
@app.route('/')
def index():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    return render_template('index.html', students=students)


# for adding students
@app.route('/add', methods = ['POST'])
def add_student():
    name = request.form['name']
    age = request.form['age']
    grade = request.form['grade']
    cursor.execute("INSERT INTO Students (name,age,grade) VALUES (%s, %s, %s)", (name, age, grade))
    db.commit()
    return redirect(url_for('index'))

#Delete Student
@app.route('/delete/<int:id>')
def delete_student(id):
    cursor.execute("DELETE FROM students WHERE id = %s", (id,))
    db.commit()

    return redirect(url_for('index'))



@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update_student(id):
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        grade = request.form['grade']

        cursor.execute(
            "UPDATE students SET name = %s, age = %s, grade = %s WHERE id=%s",
            (name,age,grade,id)
        )

        db.commit()

        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM students WHERE id=%s", (id,))
    student = cursor.fetchone()
    return render_template('update.html', student=student)


if __name__ == '__main__':
    app.run(debug=True)