import sqlite3
from datetime import datetime

STUDENTS = [
    "PERSONAL_NUMBER",
    "RANK",
    "SURNAME",
    "NAME",
    "PATRONYMIC",
    "STUDY_GROUP"
]
ATTENDANCE = [
    "PERSONAL_NUMBER",
    "SUBJECT_CODE",
    "DATE",
    "TIME"
]
SUBJECTS = [
    "CODE",
    "NAME"
]


class StudentDataWorker:
    _DATA_PATH = 'data/data2.db'
    _Instance = None

    @staticmethod
    def get_instance():
        if not (StudentDataWorker._Instance is None):
            return StudentDataWorker._Instance

        StudentDataWorker._Instance = StudentDataWorker()
        return StudentDataWorker._Instance

    def __init__(self):
        self.conn = sqlite3.connect(self._DATA_PATH, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def add_student(self,
                    personal_number: str,
                    rank: str,
                    surname: str,
                    name: str,
                    patronymic: str,
                    study_group: str):
        self.cursor.executemany("INSERT INTO STUDENTS VALUES (?, ?, ?, ?, ?, ?)", [(personal_number, rank, surname,
                                                                                    name, patronymic,
                                                                                    study_group)])
        self.conn.commit()

    def update_student(self,
                       personal_number: str,
                       rank=None,
                       surname=None,
                       name=None,
                       patronymic=None,
                       study_group=None):
        if not (rank is None or rank == ""):
            self.cursor.executemany(f"UPDATE STUDENTS SET "
                                    f"rank = (?) "
                                    f"WHERE PERSONAL_NUMBER = (?)",
                                    [(rank, personal_number)])
            self.conn.commit()
        if not (surname is None or surname == ""):
            self.cursor.executemany(f"UPDATE STUDENTS SET "
                                    f"surname = (?) "
                                    f"WHERE PERSONAL_NUMBER = (?)",
                                    [(surname, personal_number)])
            self.conn.commit()
        if not (name is None or name == ""):
            self.cursor.executemany(f"UPDATE STUDENTS SET "
                                    f"name = (?) "
                                    f"WHERE PERSONAL_NUMBER = (?)",
                                    [(name, personal_number)])
            self.conn.commit()
        if not (patronymic is None or patronymic == ""):
            self.cursor.executemany(f"UPDATE STUDENTS SET "
                                    f"patronymic = (?) "
                                    f"WHERE PERSONAL_NUMBER = (?)",
                                    [(patronymic, personal_number)])
            self.conn.commit()
        if not (study_group is None or study_group == ""):
            self.cursor.executemany(f"UPDATE STUDENTS SET "
                                    f"study_group = (?) "
                                    f"WHERE PERSONAL_NUMBER = (?)",
                                    [(study_group, personal_number)])
            self.conn.commit()

    def del_student(self,
                    personal_number: str):
        self.cursor.execute(f"DELETE FROM STUDENTS "
                            f"WHERE PERSONAL_NUMBER = \"{personal_number}\"")
        self.conn.commit()
        self.cursor.execute(f"DELETE FROM ATTENDANCE "
                            f"WHERE PERSONAL_NUMBER = \"{personal_number}\"")
        self.conn.commit()

    def add_subject(self,
                    code: str,
                    name: str):
        self.cursor.executemany("INSERT INTO SUBJECTS VALUES (?, ?)", [(code, name)])
        self.conn.commit()

    def update_subject(self,
                       code: str,
                       name=None):
        if not (name is None or name == ""):
            self.cursor.executemany(f"UPDATE SUBJECTS SET "
                                    f"name = (?) "
                                    f"WHERE CODE = (?)",
                                    [(name, code,)])
            self.conn.commit()

    def del_subject(self,
                    code: str):
        self.cursor.executemany("DELETE FROM SUBJECTS WHERE CODE = (?)", [(code,)])
        self.conn.commit()

    def mark_student(self,
                     personal_number: str,
                     subject_code: str,
                     date,
                     time):
        self.cursor.executemany("INSERT INTO ATTENDANCE VALUES (?, ?, ?, ?)", [(personal_number, subject_code,
                                                                             date, time)])
        self.conn.commit()

    def search_students(self,
                        personal_number=None,
                        rank=None,
                        surname=None,
                        name=None,
                        patronymic=None,
                        study_group=None):
        ans = []  # [{}, {}, ...]
        sql = ""
        if not (personal_number is None or personal_number == ""):
            sql += f"PERSONAL_NUMBER = \"{personal_number}\", "
        if not (rank is None or rank == ""):
            sql += f"RANK = \"{rank}\", "
        if not (surname is None or surname == ""):
            sql += f"SURNAME = \"{surname}\", "
        if not (name is None or name == ""):
            sql += f"NAME = \"{name}\", "
        if not (patronymic is None or patronymic == ""):
            sql += f"PATRONYMIC = \"{patronymic}\", "
        if not (study_group is None or study_group == ""):
            sql += f"STUDY_GROUP = \"{study_group}\", "

        if not (sql == ""):
            sql = sql[:-2].replace(',', ' AND')

            self.cursor.execute(
                f"SELECT * FROM STUDENTS WHERE {sql}")
            res = self.cursor.fetchall()  # [(), (), ...]

            for per in res:
                d = {}
                for i in range(len(per)):
                    d[STUDENTS[i]] = per[i]
                ans.append(d)

        return ans

    def get_student_history(self,
                            personal_number):
        self.cursor.execute(
            f"SELECT SUBJECT_CODE, DATE, TIME FROM ATTENDANCE WHERE personal_number = \"{personal_number}\"")
        history = self.cursor.fetchall()  # [(), (), ...]
        ans = []  # [{}, {}, ...]
        for per in history:
            d = {}
            for i in range(len(per)):
                d[ATTENDANCE[i + 1]] = per[i]
            ans.append(d)
        return ans

    def get_all_students(self):
        self.cursor.execute("SELECT * FROM STUDENTS")
        persons = self.cursor.fetchall()  # [(), (), ...]
        ans = []  # [{}, {}, ...]
        for per in persons:
            d = {}
            for i in range(len(per)):
                d[STUDENTS[i]] = per[i]
            ans.append(d)
        return ans

    def get_student_info(self,
                        personal_number: str):
        self.cursor.execute(f"SELECT * FROM STUDENTS WHERE personal_number = \"{personal_number}\"")
        person = self.cursor.fetchall()  # [()]
        ans = []  # [{}]
        for per in person:
            d = {}
            for i in range(len(per)):
                d[STUDENTS[i]] = per[i]
            ans.append(d)
        return ans
