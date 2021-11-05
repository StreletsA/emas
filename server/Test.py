import datetime
import time

from data.core.DataHelper import DataHelper
from data.core.data_worker import StudentDataWorker

if __name__ == "__main__":
    dh = DataHelper.get_instance()
    dw = StudentDataWorker.get_instance()
    print(dw.get_all_students())
