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
        print(self.data)
        return self.name

    def _create_summed_scores(self):
        score_compare = 0
        my_score = self._my_score("2020", 9)
        industries = self._get_industries() # id and industry
        for industry in industries:
            data = self._pull_all_values(2022, 9, industry['id'])
            for d in data:
                if self.industry == 'Pharmaceutical' and industry['industry'] == 'Pharmaceutical':
                    score_compare += (0.75 * float(d["electricity"]) + 0.125 * float(d["water"]) + 0.125* float(d["co2"]))
                if self.industry == 'Software & Tech Services' and industry['industry'] == 'Software & Tech Services':
                    score_compare += (0.75 * float(d["electricity"]) + 0.125 * float(d["water"]) + 0.125* float(d["co2"]))
                if self.industry == 'Electrical Equipment & Parts' and industry['industry'] == 'Electrical Equipment & Parts':
                    score_compare += (0.75 * float(d["electricity"]) + 0.125 * float(d["water"]) + 0.125* float(d["co2"]))
                if self.industry == 'Retail' and industry['industry'] == 'Retail':
                    score_compare += (0.75 * float(d["electricity"]) + 0.125 * float(d["water"]) + 0.125* float(d["co2"]))
                if self.industry == 'Insurance' and industry['industry'] == 'Insurance':
                    score_compare += (0.75 * float(d["electricity"]) + 0.125 * float(d["water"]) + 0.125* float(d["co2"]))
        score_compare = score_compare/2
        final_score = (my_score/score_compare )*100
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
        results = curs.execute("SELECT DISTINCT id, industry FROM company")
        data = results.fetchall()
        conn.close()
        return data

    def _my_score(self, year, month):

        prev_month, prev_elec, curr_month, elec = get_values(self.data, year, month)
        prev_month, prev_value, curr_month, water = get_values(self.data, year, month, type = "water")
        prev_month, prev_value, curr_month, co2 = get_values(self.data, year, month, type = "co2")
        return (0.75 * float(elec) + 0.125 * float(water) + 0.125* float(co2))
    
c = Company("sbb", 0, "Retail", "foo")

final = c._create_summed_scores()
print(final)