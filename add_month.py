import sqlite3
import numpy as np

def add_months(year, current_month, months):
    year_flip = False
    connection = sqlite3.connect('database.db')
    cur = connection.cursor()
    for company in range(11):
            for month in range(months):
                if month+current_month and not year_flip > 12:
                    year+=1
                electricity = round(1000 + round(np.random.random(), 2)*150 * np.random.choice([-1, 1, 1, 1]), 1)
                water = round(5 + round(np.random.random(), 2)*150 * np.random.choice([-1, 1, 1, 1]), 1)
                co2 = round(3 + round(np.random.random(), 2)*150 * np.random.choice([-1, 1, 1, 1]), 1)
                cur.execute("INSERT INTO consumptions (company_id, year, month, electricity, water, co2) VALUES (?, ?, ?, ?, ?, ?)",
                        (company, year, (month+current_month+12)%12, electricity, water, co2))