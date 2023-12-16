import csv
from db import database

db = database.BotDataBase('database.db')
with open('file.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        if not row[0] == 'id':
            print(row)
            # db.add_suggestion(row[1], int(row[2]), row[3], row[4], row[5], row[8], row[6], row[7], row[9], row[10])
            # db.approve_suggestion(int(row[0]), int(row[2]))
