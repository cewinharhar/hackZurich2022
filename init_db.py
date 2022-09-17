import sqlite3
import numpy as np

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

def initCompany():
    cur = connection.cursor()
    cur.execute("INSERT INTO company (name, industry, summary) VALUES (?, ?, ?)", 
                ('Novartis', 'Industry X', 'Descriptio cation when wher summary xy the company did'))
    cur.execute("INSERT INTO company (name, industry, summary) VALUES (?, ?, ?)",
        ('Zühlke', 'Industry Y', 'Descriptio cation when wher summary xy the company did'))
    connection.commit()

def initConsumptions():
    cur = connection.cursor()
    data = []
    for company in range(11): 
        increaseValue = 0.1
        for year in range(2000, 2023): 
            for month in range(1,13):
                increaseValue = increaseValue + round(np.random.random(), 1) / 10

                electricity = round(10 + increaseValue + np.random.choice([-1, 1, 1, 1]), 1)
                water = round(5 + increaseValue + np.random.choice([-1, 1, 1, 1]), 1)
                co2 = round(3 + increaseValue + np.random.choice([-1, 1, 1, 1, 1, 1]), 1)


                data.append([company, year, month, electricity, water, co2])

                cur.execute("INSERT INTO consumptions (company_id, year, month, electricity, water, co2) VALUES (?, ?, ?, ?, ?, ?)",
                        (company, year, month, electricity, water, co2))

    connection.commit()

initCompany()
initConsumptions()

connection.close()