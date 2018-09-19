from utils import create_csv
import os

current_path = os.getcwd()
create_csv.CreateCsv(current_path + "/face_database/")
