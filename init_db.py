import sqlite3
import numpy as np

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

def initCompany():
    cur = connection.cursor()
    cur.execute("INSERT INTO company (name, industry, summary) VALUES (?, ?, ?)", 
                ('Novartis', 'Pharmaceutical', ', Novartis is an international leader in the development and marketing of pharmaceuticals and nutrition products, in addition to operating a number of research institutes dedicated to the study of gene therapy.'))

    cur.execute("INSERT INTO company (name, industry, summary) VALUES (?, ?, ?)",
                ('Zühlke', 'Software & Tech Services', 'Zühlke is a global innovation service provider. They envisage ideas and create new business models for clients by developing services and products based on new technologies – from the initial vision through development to deployment, production and operation. They specialise in strategy and business innovation, digital solutions and application services – in addition to device and systems engineering.))

    cur.execute("INSERT INTO company (name, industry, summary) VALUES (?, ?, ?)",
                ('ABB', 'Electrical Equipment & Parts', 'ABB Limited provides power and automation technologies. The Company operates under segments that include power products, power systems, automation products, process automation, and robotics.'))

    cur.execute("INSERT INTO company (name, industry, summary) VALUES (?, ?, ?)",
                ('Migros', 'Retail', 'ABB Limited provides power and automation technologies. The Company operates under segments that include power products, power systems, automation products, process automation, and robotics.'))

    cur.execute("INSERT INTO company (name, industry, summary) VALUES (?, ?, ?)",
                ('Swiss Re', 'Retail', 'ABB Limited provides power and automation technologies. The Company operates under segments that include power products, power systems, automation products, process automation, and robotics.'))

    cur.execute("INSERT INTO company (name, industry, summary) VALUES (?, ?, ?)",
                ('Migros', 'Retail', 'ABB Limited provides power and automation technologies. The Company operates under segments that include power products, power systems, automation products, process automation, and robotics.'))



    connection.commit()

def initConsumptions():
    cur = connection.cursor()
    data = []
    for company in range(11): 
        increaseValue = 0.1
        for year in range(2001, 2023): 
            for month in range(13):
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