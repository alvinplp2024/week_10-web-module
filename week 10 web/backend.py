from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Connect to SQLite database
conn = sqlite3.connect('course_selection.db')
cursor = conn.cursor()

# Create tables if not exist
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    password TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    description TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS user_courses (
                    user_id INTEGER,
                    course_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (course_id) REFERENCES courses(id),
                    PRIMARY KEY (user_id, course_id)
                )''')

# Close cursor and connection
cursor.close()
conn.close()

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Check login credentials
        username = request.form['username']
        password = request.form['password']
        # Implement your authentication logic here
        # Assuming authentication is successful, redirect to course selection
        return redirect(url_for('select_courses'))
    return render_template('login.html')

# Route for selecting courses
@app.route('/courses', methods=['GET', 'POST'])
def select_courses():
    conn = sqlite3.connect('course_selection.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        # Get selected courses from form
        selected_courses = request.form.getlist('course')
        user_id = 1  # Assuming user ID 1 for simplicity, you'd use the logged-in user's ID
        # Store selected courses in database
        for course_id in selected_courses:
            cursor.execute("INSERT INTO user_courses (user_id, course_id) VALUES (?, ?)", (user_id, course_id))
        conn.commit()
        conn.close()
        return redirect(url_for('display_selected_courses'))

    # Fetch available courses
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    conn.close()
    return render_template('courses.html', courses=courses)

# Route for displaying selected courses
@app.route('/selected_courses')
def display_selected_courses():
    conn = sqlite3.connect('course_selection.db')
    cursor = conn.cursor()
    user_id = 1  # Assuming user ID 1 for simplicity, you'd use the logged-in user's ID
    # Fetch selected courses for the logged-in user
    cursor.execute("SELECT c.name, c.description FROM user_courses uc JOIN courses c ON uc.course_id = c.id WHERE uc.user_id = ?", (user_id,))
    selected_courses = cursor.fetchall()
    conn.close()
    return render_template('selected_courses.html', selected_courses=selected_courses)

if __name__ == '__main__':
    app.run(debug=True)
