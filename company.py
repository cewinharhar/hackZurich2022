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

    # def monthly_difference(self, year, month):
    #     self.data

######
# to show the order of results
######

# c = Company("sbb", 1, "bar", "fooo")

# prev_month, prev_elec, curr_month, curr_elec = get_values(c.data, "2010", 5)

# print(prev_month, prev_elec, curr_month, curr_elec)