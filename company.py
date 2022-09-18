# class with all the fields of the company
# in the main class for each field i need to call a mthod for that 
# specific field and sumarize into a dictionary

# imports
from db import *
from utils import *
import numpy as np
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
        elecLast = get_values_by_year_and_type_and_comp(last_year['year'], 'electricity', self.id)
        waterLast = get_values_by_year_and_type_and_comp(last_year['year'], 'water', self.id)

        elecMean = statistics.mean(elecLast[:-1])
        waterMean = statistics.mean(waterLast[:-1])

        # industries = self._get_industries() # id and industry
        # last_month = last_month['month']
        # prev_month = last_month - 1
        # last_year = last_year['year']
        # year = last_year
        my_score_elec, my_score_water = self._my_score(str(last_year['year']), last_month['month'])
    
        # if last_month == 1:
        #     prev_month = 12
        #     year -= 1
     
        final_score = (0.75*(my_score_elec - elecMean) + 0.25*(my_score_water - waterMean))
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
        return elec, water


