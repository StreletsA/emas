"""
    !!!DEPRECATED!!!
"""

import os
import sqlite3
from datetime import datetime

person_info_columns = [
    "personal_number",
    "rank",
    "surname",
    "name",
    "patronymic",
    "study_group"
]
identity_columns = [
    "personal_number",
    "finger_print"
]
check_table_columns = [
    "personal_number",
    "classroom_number",
    "check_time"
]

class DataHelper:
    _DATA_PATH = 'data/data.db'
    _Instance = None

    @staticmethod
    def get_instance():
        if not (DataHelper._Instance is None):
            return DataHelper._Instance

        DataHelper._Instance = DataHelper()
        return DataHelper._Instance

    def __init__(self):
        self.conn = sqlite3.connect(self._DATA_PATH, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def add_person_info(self,
                        personal_number: str,
                        rank: str,
                        surname: str,
                        name: str,
                        patronymic: str,
                        study_group: str):
        self.cursor.executemany("INSERT INTO person_info VALUES (?, ?, ?, ?, ?, ?)", [(personal_number, rank, surname,
                                                                                       name, patronymic,
                                                                                       study_group)])
        self.conn.commit()

    def add_to_identity(self,
                        personal_number: str,
                        finger_print):
        self.cursor.executemany("INSERT INTO identity VALUES (?, ?)", [(personal_number, finger_print)])
        self.conn.commit()

    def _add_to_check_table(self,
                            personal_number: str,
                            classroom_number: str,
                            check_time: datetime):
        self.cursor.executemany("INSERT INTO check_table VALUES (?, ?, ?)", [(personal_number, classroom_number,
                                                                              check_time)])
        self.conn.commit()

    def _get_person_checking_history(self,
                                     personal_number: str):
        self.cursor.execute(
            f"SELECT classroom_number, check_time FROM check_table WHERE personal_number = \"{personal_number}\"")
        return self.cursor.fetchall()

    def add_person(self,
                   personal_number: str,
                   rank: str,
                   surname: str,
                   name: str,
                   patronymic: str,
                   study_group: str,
                   finger_print):
        self.add_person_info(personal_number,
                             rank,
                             surname,
                             name,
                             patronymic,
                             study_group)

        self.add_to_identity(personal_number,
                             finger_print)

    def mark_person(self,
                    personal_number: str,
                    classroom_number: str,
                    check_time: datetime):
        self._add_to_check_table(personal_number,
                                 classroom_number,
                                 check_time)

    def update_person(self,
                      personal_number: str,
                      rank: str,
                      surname: str,
                      name: str,
                      patronymic: str,
                      study_group: str,
                      finger_print):
        self.cursor.execute(f"UPDATE person_info SET "
                            f"rank = \"{rank}\", "
                            f"surname = \"{surname}\", "
                            f"name = \"{name}\", "
                            f"patronymic = \"{patronymic}\", "
                            f"study_group = \"{study_group}\" "
                            f"WHERE personal_number = \"{personal_number}\"")
        self.conn.commit()
        self.cursor.execute(f"UPDATE identity SET "
                            f"finger_print = \"{finger_print}\" "
                            f"WHERE personal_number = \"{personal_number}\"")
        self.conn.commit()

    def delete_person(self,
                      personal_number: str):
        self.cursor.execute(f"DELETE FROM person_info "
                            f"WHERE personal_number = \"{personal_number}\"")
        self.conn.commit()
        self.cursor.execute(f"DELETE FROM identity "
                            f"WHERE personal_number = \"{personal_number}\"")
        self.conn.commit()
        self.cursor.execute(f"DELETE FROM check_table "
                            f"WHERE personal_number = \"{personal_number}\"")
        self.conn.commit()

    def search_persons(self,
                   personal_number: str,
                   rank: str,
                   surname: str,
                   name: str,
                   patronymic: str,
                   study_group: str):
        ans = []  # [{}, {}, ...]
        sql = ""
        if not (personal_number is None or personal_number == ""):
            sql += f"personal_number = \"{personal_number}\", "
        if not (rank is None or rank == ""):
            sql += f"rank = \"{rank}\", "
        if not (surname is None or surname == ""):
            sql += f"surname = \"{surname}\", "
        if not (name is None or name == ""):
            sql += f"name = \"{name}\", "
        if not (patronymic is None or patronymic == ""):
            sql += f"patronymic = \"{patronymic}\", "
        if not (study_group is None or study_group == ""):
            sql += f"study_group = \"{study_group}\", "

        if not (sql == ""):
            sql = sql[:-1]
            self.cursor.execute(
                f"SELECT * FROM person_info WHERE {sql[:-1]}")
            res = self.cursor.fetchall()  # [(), (), ...]

            for per in res:
                d = {}
                for i in range(len(per)):
                    d[person_info_columns[i]] = per[i]
                ans.append(d)

        return ans

    def get_person_history(self,
                           personal_number):
        history = self._get_person_checking_history(personal_number)  # [(), (), ...]
        ans = []  # [{}, {}, ...]
        for per in history:
            d = {}
            for i in range(len(per)):
                d[check_table_columns[i + 1]] = per[i]
            ans.append(d)
        return ans

    def get_all_persons_info(self):
        self.cursor.execute("SELECT * FROM person_info")
        persons = self.cursor.fetchall()  # [(), (), ...]
        ans = []  # [{}, {}, ...]
        for per in persons:
            d = {}
            for i in range(len(per)):
                d[person_info_columns[i]] = per[i]
            ans.append(d)
        return ans

    def get_person_info(self,
                        personal_number: str):
        self.cursor.execute(f"SELECT * FROM person_info WHERE personal_number = \"{personal_number}\"")
        person = self.cursor.fetchall()  # [()]
        ans = []  # [{}]
        for per in person:
            d = {}
            for i in range(len(per)):
                d[person_info_columns[i]] = per[i]
            ans.append(d)
        return ans
