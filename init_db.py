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

cur.execute("INSERT INTO company (name, industry) VALUES (?, ?)",
            ('Novartis', 'Industry X')
            )

cur.execute("INSERT INTO company (name, industry) VALUES (?, ?)",
            ('Zühlke', 'Industry Y')
            )

cur.execute("INSERT INTO company (name, industry) VALUES (?, ?)",
            ('Novartis', 'Industry X')
            )

cur.execute("INSERT INTO company (name, industry) VALUES (?, ?)",
            ('Zühlke', 'Industry Y')
            )

cur.execute("INSERT INTO company (name, industry) VALUES (?, ?)",
            ('Novartis', 'Industry X')
            )

cur.execute("INSERT INTO company (name, industry) VALUES (?, ?)",
            ('Zühlke', 'Industry Y')
            )

cur.execute("INSERT INTO company (name, industry) VALUES (?, ?)",
            ('Novartis', 'Industry X')
            )

cur.execute("INSERT INTO company (name, industry) VALUES (?, ?)",
            ('Zühlke', 'Industry Y')
            )

cur.execute("INSERT INTO consumptions (company_id, year, month, electricity, water, co2) VALUES (?, ?, ?, ?, ?, ?)",
            ('1', '2020', '12', '453', '234', '11')
            )

cur.execute("INSERT INTO consumptions (company_id, year, month, electricity, water, co2) VALUES (?, ?, ?, ?, ?, ?)",
            ('1', '2020', '11', '4533', '4', '10')
            )
cur.execute("INSERT INTO consumptions (company_id, year, month, electricity, water, co2) VALUES (?, ?, ?, ?, ?, ?)",
            ('1', '2020', '10', '43', '2134', '121')
            )
cur.execute("INSERT INTO consumptions (company_id, year, month, electricity, water, co2) VALUES (?, ?, ?, ?, ?, ?)",
            ('1', '2020', '9', '4533', '34', '111')
            )
connection.commit()
connection.close()
