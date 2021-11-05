from server_api import app as api_app
from flask import Flask, jsonify
from flask import request
from data.core.DataHelper import DataHelper
from datetime import datetime
from flask import render_template

app = Flask(__name__, template_folder="templates")

data_helper = DataHelper.get_instance()


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
                           title='Система контроля обучения')


@app.route('/lcs/api/persons/', methods=['GET'])
def get_persons():
    ans = data_helper.get_all_persons_info()
    return jsonify({'persons': ans})


@app.route('/lcs/api/persons/<string:personal_number>', methods=['GET'])
def get_person_info(personal_number):
    ans = data_helper.get_person_info(personal_number)
    return jsonify({'person': ans})


@app.route('/lcs/api/persons/history/<string:personal_number>', methods=['GET'])
def get_person_history(personal_number):
    ans = data_helper.get_person_history(personal_number)
    return jsonify({personal_number: ans})


# .../mark?personal_number=...&classroom_number=...&year=...&month=...&day=...&hh=...&mm=...&ss=...
@app.route('/lcs/api/persons/mark/', methods=['GET'])
def mark_person():
    try:
        personal_number = request.args.get('personal_number')
        classroom_number = request.args.get('classroom_number')
        year = request.args.get('year')
        month = request.args.get('month')
        day = request.args.get('day')
        hh = request.args.get('hh')
        mm = request.args.get('mm')
        ss = request.args.get('ss')

        for i in [personal_number, classroom_number, year, month, day, hh, mm, ss]:
            if i is None:
                return jsonify({'result': 'one of parameters is None'})

        dt = datetime(int(year), int(month), int(day), int(hh), int(mm), int(ss))

        data_helper.mark_person(personal_number, classroom_number, dt)

    except Exception as e:
        return jsonify({'result': False})

    return jsonify({'result': True})


# .../add?personal_number=...&rank=...&surname=...&name=...&patronymic=...&study_group=...&finger_print=...
@app.route('/lcs/api/persons/add/', methods=['GET'])
def add_person():
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

        data_helper.add_person(personal_number, rank, surname, name, patronymic, study_group, finger_print)

    except Exception as e:
        return jsonify({'result': False})

    return jsonify({'result': True})


# .../update?personal_number=...&rank=...&surname=...&name=...&patronymic=...&study_group=...&finger_print=...
@app.route('/lcs/api/persons/update/', methods=['GET'])
def update_person():
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

        data_helper.update_person(personal_number, rank, surname, name, patronymic, study_group, finger_print)

    except Exception as e:
        return jsonify({'result': False})

    return jsonify({'result': True})

# .../delete?personal_number=...
@app.route('/lcs/api/persons/delete/', methods=['GET'])
def delete_person():
    try:
        personal_number = request.args.get('personal_number')

        for i in [personal_number]:
            if i is None:
                return jsonify({'result': 'one of parameters is None'})

        data_helper.delete_person(personal_number)

    except Exception as e:
        return jsonify({'result': False})

    return jsonify({'result': True})

# .../delete?personal_number=...&rank=...&surname=...&name=...&patronymic=...&study_group=...
@app.route('/lcs/api/persons/search/', methods=['GET'])
def search_persons():
    ans = []
    try:
        personal_number = request.args.get('personal_number')
        rank = request.args.get('rank')
        surname = request.args.get('surname')
        name = request.args.get('name')
        patronymic = request.args.get('patronymic')
        study_group = request.args.get('study_group')

        ans = data_helper.search_persons(personal_number, rank, surname, name, patronymic, study_group)

    except Exception as e:
        return jsonify({'result': str(e)})

    return jsonify({'persons': ans})

if __name__ == "__main__":
    app.run(debug=True)
    api_app.run(debug=True)
