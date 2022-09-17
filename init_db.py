import sqlite3
import numpy as np

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

def initCompany():
    cur = connection.cursor()
    cur.execute("INSERT INTO company (name, industry, summary) VALUES (?, ?, ?)", 
                ('Novartis', 'Pharmaceutical', 'Novartis is an international leader in the development and marketing of pharmaceuticals and nutrition products, in addition to operating a number of research institutes dedicated to the study of gene therapy.'))

    cur.execute("INSERT INTO company (name, industry, summary) VALUES (?, ?, ?)", 
                ('Roche', 'Pharmaceutical', 'Roche has grown into one of the worlds largest biotech companies, as well as a leading provider of in-vitro diagnostics and a global supplier of transformative innovative solutions across major disease areas. '))

    cur.execute("INSERT INTO company (name, industry, summary) VALUES (?, ?, ?)",
                ('Zühlke', 'Software & Tech Services', 'Zühlke is a global innovation service provider. They envisage ideas and create new business models for clients by developing services and products based on new technologies – from the initial vision through development to deployment, production and operation. They specialise in strategy and business innovation, digital solutions and application services – in addition to device and systems engineering.'))

    cur.execute("INSERT INTO company (name, industry, summary) VALUES (?, ?, ?)",
                ('Google', 'Software & Tech Services', 'Google LLC (Google), a subsidiary of Alphabet Inc, is a provider of search and advertising services on the internet. The company focuses on business areas such as advertising, search, platforms and operating systems, and enterprise and hardware products.'))

    cur.execute("INSERT INTO company (name, industry, summary) VALUES (?, ?, ?)",
                ('ABB', 'Electrical Equipment & Parts', 'ABB Limited provides power and automation technologies. The Company operates under segments that include power products, power systems, automation products, process automation, and robotics.'))

    cur.execute("INSERT INTO company (name, industry, summary) VALUES (?, ?, ?)",
                ('Emerson', 'Electrical Equipment & Parts', 'Emersons two core business platforms — Automation Solutions and Commercial & Residential Solutions — allow us to identify and confront the challenges of an increasingly complex and unpredictable marketplace from a position of strength, driving near- and long-term value as a trusted partner for our customers.'))

    cur.execute("INSERT INTO company (name, industry, summary) VALUES (?, ?, ?)",
                ('Migros', 'Retail', 'Migros consumer and service products are oriented to everyday needs, to all levels of society and their specific needs regarding quality of life.'))

    cur.execute("INSERT INTO company (name, industry, summary) VALUES (?, ?, ?)",
                ('Lidl', 'Retail', 'We are a successful chain of grocery stores and have been expanding strongly throughout Europe for over 40 years. Lidl currently operates around 12,000 stores and more than 200 goods distribution and logistics centers in 31 countries, offering top-quality food and non-food products at the best price.'))

    cur.execute("INSERT INTO company (name, industry, summary) VALUES (?, ?, ?)",
                ('Swiss Re', 'Insurance', 'ABB Limited provides power and automation technologies. The Company operates under segments that include power products, power systems, automation products, process automation, and robotics.'))

    cur.execute("INSERT INTO company (name, industry, summary) VALUES (?, ?, ?)",
                ('Zurich ', 'Insurance', 'Zurich is a leading multi-line insurer that serves its customers in global and local markets. With about 56,000 employees, it provides a wide range of property and casualty, life insurance products and services in more than 210 countries and territories. Zurichs customers include individuals, small businesses, and mid-sized and large companies, as well as multinational corporations.'))

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