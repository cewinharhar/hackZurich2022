import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO company (name, industry) VALUES (?, ?)",
            ('Novartis', 'Industry X')
            )

cur.execute("INSERT INTO company (name, industry) VALUES (?, ?)",
            ('Zühlke', 'Industry Y')
            )

cur.execute("INSERT INTO consumptions (company_id, year, month, elecricity, water, co2) VALUES (?, ?, ?, ?, ?, ?)",
            ('1', '2020', '12', '453', '234', '11')
            )

connection.commit()
connection.close()
