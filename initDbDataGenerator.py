from ast import increment_lineno
from logging.handlers import WatchedFileHandler
import numpy as np

import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

def initDbDataGenerator():
    data = []
    for company in range(11): 
        increaseValue = 0.1
        for year in range(2000, 2021): 
            for month in range(13):
                increaseValue = increaseValue + round(np.random.random(), 1) / 10

                electricity = round(10 + increaseValue + np.random.choice([-1, 1, 1, 1]), 1)
                water = round(5 + increaseValue + np.random.choice([-1, 1, 1, 1]), 1)
                co2 = round(3 + increaseValue + np.random.choice([-1, 1, 1, 1, 1, 1]), 1)


                data.append([company, year, month, electricity, water, co2])

    cur.execute("INSERT INTO consumptions (company_id, year, month, electricity, water, co2) VALUES (?, ?, ?, ?, ?, ?)",
            (company, year, month, electricity, water, co2))
                        
