from flask import Flask, jsonify
from flask import request
from flask import render_template
from data.core.data_worker import StudentDataWorker
from datetime import datetime
import os
from flask_cors import CORS, cross_origin

app = Flask(__name__)

student_dw = StudentDataWorker.get_instance()

"""
    EMAS -> Education Monitoring and Analyzing System
"""

"""
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
                           title='Система контроля обучения')
"""

@app.route('/emas/api/students/', methods=['GET'])
@cross_origin()
def get_students():
    ans = student_dw.get_all_students()
    return jsonify({'students': ans})


@app.route('/emas/api/students/<string:personal_number>', methods=['GET'])
@cross_origin()
def get_student_info(personal_number):
    ans = student_dw.get_student_info(personal_number)
    return jsonify({'student': ans})


@app.route('/emas/api/students/history/<string:personal_number>', methods=['GET'])
@cross_origin()
def get_student_history(personal_number):
    ans = student_dw.get_student_history(personal_number)
    return jsonify({personal_number: ans})


# .../mark?personal_number=...&subject_code=...&year=...&month=...&day=...&hh=...&mm=...&ss=...
@app.route('/emas/api/students/mark/', methods=['GET'])
@cross_origin()
def mark_student():
    try:
        personal_number = request.args.get('personal_number')
        subject_code = request.args.get('subject_code')
        year = request.args.get('year')
        month = request.args.get('month')
        day = request.args.get('day')
        hh = request.args.get('hh')
        mm = request.args.get('mm')
        ss = request.args.get('ss')

        for i in [personal_number, subject_code, year, month, day, hh, mm, ss]:
            if i is None:
                return jsonify({'result': 'one of parameters is None'})

        dt = datetime(int(year), int(month), int(day), int(hh), int(mm), int(ss))

        student_dw.mark_student(personal_number, subject_code, dt.date(), dt.time())

    except Exception as e:
        return jsonify({'result': False})

    return jsonify({'result': True})


# .../add?personal_number=...&rank=...&surname=...&name=...&patronymic=...&study_group=...&finger_print=...
@app.route('/emas/api/students/add/', methods=['GET'])
@cross_origin()
def add_student():
    try:
        personal_number = request.args.get('personal_number')
        rank = request.args.get('rank')
        surname = request.args.get('surname')
        name = request.args.get('name')
        patronymic = request.args.get('patronymic')
        study_group = request.args.get('study_group')
        finger_print = request.args.get('finger_print')

        for i in [personal_number, rank, surname, name, patronymic, study_group, finger_print]:
            if i is None:
                return jsonify({'result': 'one of parameters is None'})

        student_dw.add_student(personal_number, rank, surname, name, patronymic, study_group, finger_print)

    except Exception as e:
        return jsonify({'result': False})

    return jsonify({'result': True})


# .../update?personal_number=...&rank=...&surname=...&name=...&patronymic=...&study_group=...&finger_print=...
@app.route('/emas/api/students/update/', methods=['GET'])
@cross_origin()
def update_student():
    try:
        personal_number = request.args.get('personal_number')
        rank = request.args.get('rank')
        surname = request.args.get('surname')
        name = request.args.get('name')
        patronymic = request.args.get('patronymic')
        study_group = request.args.get('study_group')
        finger_print = request.args.get('finger_print')

        for i in [personal_number, rank, surname, name, patronymic, study_group, finger_print]:
            if i is None:
                return jsonify({'result': 'one of parameters is None'})

        student_dw.update_student(personal_number, rank, surname, name, patronymic, study_group, finger_print)

    except Exception as e:
        return jsonify({'result': False})

    return jsonify({'result': True})

# .../delete?personal_number=...
@app.route('/emas/api/students/delete', methods=['GET'])
@cross_origin()
def delete_student():
    try:
        personal_number = request.args.get('personal_number')
        for i in [personal_number]:
            if i is None:
                return jsonify({'result': 'one of parameters is None'})

        student_dw.del_student(personal_number)
    except Exception as e:
        return jsonify({'result': str(e)})

    return jsonify({'result': True})


# .../delete?personal_number=...&rank=...&surname=...&name=...&patronymic=...&study_group=...
@app.route('/lcs/api/persons/search', methods=['GET'])
@cross_origin()
def search_students():
    ans = []
    try:
        personal_number = request.args.get('personal_number')
        rank = request.args.get('rank')
        surname = request.args.get('surname')
        name = request.args.get('name')
        patronymic = request.args.get('patronymic')
        study_group = request.args.get('study_group')

        ans = student_dw.search_students(personal_number, rank, surname, name, patronymic, study_group)

    except Exception as e:
        return jsonify({'result': str(e)})

    return jsonify({'students': ans})

if __name__ == "__main__":
    app.run(debug=True)