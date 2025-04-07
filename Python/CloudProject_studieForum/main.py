import random
import db_stud
import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'databases/login.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret-key'
db = SQLAlchemy()
db.init_app(app)


study_room_db = db_stud.StudyRoomDB()


@app.route('/')
def index():
    return render_template("index.html", courses=study_room_db.courses)


@app.route('/courses')
def courses():
    return render_template("courses.html", courses=study_room_db.courses)


@app.route('/courses/info')
def courses_info():
    course_id = request.args["course_id"]
    connection = db_stud.open_connection("studyroom")
    course_entry = db_stud.get_course_with_id(connection=connection, course_id=course_id)
    print(course_entry)
    course = {"id": course_id,
              "name": course_entry[0][1],
              "info": course_entry[0][2]}
    return render_template("course_info.html", course=course, courses=study_room_db.courses)


@app.route('/quizes')
def quizes():
    return render_template("quizes.html", courses=study_room_db.courses)


@app.route('/quizes/add')
def quizes_add():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("quiz_add.html", courses=study_room_db.courses)


@app.route('/quizes/quiz_time')
def quiz_time():
    return render_template("take_quiz.html", courses=study_room_db.courses)


@app.route('/quizes/quiz_time/<course_id>/quiz')
def quizes_take(course_id):
    connection = db_stud.open_connection("studyroom")
    questions = db_stud.get_quest_for_id(connection, course_id)
    rand_question = questions[random.randint(0, len(questions) - 1)]
    course_entry = db_stud.get_course_with_id(connection=connection, course_id=course_id)
    course = {"id": course_id,
              "name": course_entry[0][1]}
    print(questions)
    return render_template("course_quiz.html", question=rand_question, course=course, courses=study_room_db.courses)


@app.route('/quizes/quiz_time/<course_id>/quiz/next_question')
def new_question(course_id):
    return redirect(f'/quizes/quiz_time/{course_id}/quiz')


@app.route('/add_question', methods=["POST"])
def add_question():
    if 'username' not in session:
        print('I got in here')
        return redirect(url_for('login'))
    question = request.form["question"]
    answer = request.form["answer"]
    course = request.form["course_slct"]

    connection = db_stud.open_connection("studyroom")
    db_stud.insert_query(connection, table="quizes",
                         value_ids="(course_id, topic, question, answer)",
                         values=f"""
                         ((SELECT course_id FROM courses WHERE name='{course}'), 
                         'None',
                         '{question}',
                         '{answer}')
                         """)

    return redirect('/quizes/add')


@app.route('/login')
def login():
    try:
        success = request.args['success']
        fail = request.args['error']
    except KeyError as e:
        success = None
        fail = None
    if success:
        return render_template('login.html', success=success)
    elif fail:
        return render_template('login.html', error=fail)
    else:
        return render_template('login.html')


@app.route('/profile')
def profile():
    return render_template("profile.html")



@app.route('/login_user', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']


    connection = db_stud.open_connection('login')
    if db_stud.user_is_valid(connection, username, password):
        session['username'] = request.form['username']
        return redirect(url_for('index', success='You successfully logged in'))
    else:
        return redirect(url_for('login', error='Invalid username or password'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index', success='You successfully logged out'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
