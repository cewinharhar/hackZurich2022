# class with all the fields of the company
# in the main class for each field i need to call a mthod for that 
# specific field and sumarize into a dictionary

# imports
from db import get_db_connection
from utils import *
class Company:
    def __init__(self, name, company_id, industry, summary):

        # initalize the class with:
        self.name = name
        self.industry = industry
        self.id = company_id
        self.summary = summary

        # fetch from database:
        self.years =self._get_year()
        self.data = self._create_data()
        self.score = self._create_summed_scores()

    def _create_data(self):
        conn = get_db_connection()
        curs = conn.cursor()
        
        dictionary = []
        # dictionary = {year: [month, elec, water, co2]}
        for year in self.years:
            results = curs.execute("SELECT month, electricity, water, co2 FROM consumptions WHERE company_id = ? and year = ?",(self.id, year["year"]))
            data = results.fetchall()
            consumption = []
            for d in data:
                # data_structure[str(year)]
                consumption.append({"month": d["month"], "electricity": d["electricity"], "water": d["water"], "co2": d["co2"]})
            # for year in self.years:
            dictionary.append({str(year["year"]): consumption})
        conn.close()
        # print(dictionary)
        return dictionary

    def _get_year(self):
        conn = get_db_connection()
        curs = conn.cursor()
        results = curs.execute("SELECT DISTINCT year FROM consumptions WHERE company_id = ?",(self.id,))
        data = results.fetchall()
        conn.close()
        return data

    def __str__(self):
        #print(self.data)
        return str(self.score)

    def _create_summed_scores(self):
        
        connection = get_db_connection()
        last_year = connection.execute('SELECT DISTINCT year FROM consumptions ORDER BY year DESC').fetchone()
        last_month = connection.execute('SELECT DISTINCT month FROM consumptions where year = ? ORDER BY month DESC', (last_year['year'],)).fetchone()
        
        industries = self._get_industries() # id and industry
        last_month = last_month['month']
        prev_month = last_month - 1
        last_year = last_year['year']
        year = last_year
        my_score = self._my_score(str(last_year), last_month)
        score_compare = 0
        if last_month == 1:
            prev_month = 12
            year -= 1
        count = 0
        for industry in industries:
            data = self._pull_all_values(last_year, last_month, industry['id'])
            data2 = self._pull_all_values(year, prev_month, industry['id'])
            for d, d2 in zip(data, data2):
                if self.industry == 'Pharmaceutical' and industry['industry'] == 'Pharmaceutical':
                    score_compare += (0.75 * (float(d["electricity"]) - float(d2["electricity"])) + 0.125 * (float(d["water"]) - float(d2["water"])))
                if self.industry == 'Software & Tech Services' and industry['industry'] == 'Software & Tech Services':
                    score_compare += (0.75 * (float(d["electricity"]) - float(d2["electricity"])) + 0.125 * (float(d["water"]) -float(d2["water"])))
                if self.industry == 'Electrical Equipment & Parts' and industry['industry'] == 'Electrical Equipment & Parts':
                    score_compare += (0.75 * (float(d["electricity"]) - float(d2["electricity"])) + 0.125 * (float(d["water"]) -float(d2["water"])))
                if self.industry == 'Retail' and industry['industry'] == 'Retail':
                    score_compare += (0.75 * (float(d["electricity"]) - float(d2["electricity"])) + 0.125 * (float(d["water"]) -float(d2["water"])))
                if self.industry == 'Insurance' and industry['industry'] == 'Insurance':
                    score_compare += (0.75 * (float(d["electricity"]) - float(d2["electricity"])) + 0.125 * (float(d["water"]) -float(d2["water"])))
                
        score_compare = score_compare/2
        final_score = int((my_score/score_compare)*100)
        connection.close()
        return final_score

    def _pull_all_values(self, year, month, id):
        conn = get_db_connection()
        curs = conn.cursor()
        results = curs.execute("SELECT electricity, water, co2 FROM consumptions WHERE year = ? and month = ? and company_id = ?", (year, month, id))
        data = results.fetchall()
        conn.close()
        return data

    def _get_industries(self):
        conn = get_db_connection()
        curs = conn.cursor()
        results = curs.execute("SELECT id, industry FROM company")
        data = results.fetchall()
        conn.close()
        return data

    def _my_score(self, year, month):
        prev_month, prev_elec, curr_month, elec = get_values(self.data, year, month)
        prev_month, prev_water, curr_month, water = get_values(self.data, year, month, type = "water")
        return (0.75 * (float(elec) - float(prev_elec)) + 0.25 * (float(water) - float(prev_water)))
