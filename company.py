# class with all the fields of the company
# in the main class for each field i need to call a mthod for that 
# specific field and sumarize into a dictionary

# imports
from db import get_db_connection, dict_factory, get_company, get_consumptions

class Company:
    def __init__(self, name, company_id, industry, summary):

        # initalize the class with:
        self.name = name
        self.industry = industry
        self.id = company_id
        self.summary = summary

        # fetch from database:

        #self.elecs = self._get_electricity()
        #self.waters = self._get_water()
        #self.co2s = self._get_co2()
        self.years =self._get_year()
       # self.months = self._get_month()
        
        # the structure:

        # {year: {"month" : 1, "elec": x, "water": x, "co2": x }}
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

    # def _get_electricity(self):
    #     conn = get_db_connection()
    #     curs = conn.cursor()
    #     results = curs.execute("SELECT electricity FROM consumptions WHERE company_id = ?",(self.id,))
    #     data = results.fetchall()
    #     conn.close()
    #     return data

    # def _get_water(self):
    #     conn = get_db_connection()
    #     curs = conn.cursor()
    #     results = curs.execute("SELECT water FROM consumptions WHERE company_id = ?",(self.id,))
    #     data = results.fetchall()
    #     conn.close()
    #     return data

    # def _get_co2(self):
    #     conn = get_db_connection()
    #     curs = conn.cursor()
    #     results = curs.execute("SELECT co2 FROM consumptions WHERE company_id = ?",(self.id,))
    #     data = results.fetchall()
    #     conn.close()
    #     return data

    def _get_year(self):
        conn = get_db_connection()
        curs = conn.cursor()
        results = curs.execute("SELECT DISTINCT year FROM consumptions WHERE company_id = ?",(self.id,))
        data = results.fetchall()
        conn.close()
        return data

    # def _get_month(self):
    #     conn = get_db_connection()
    #     curs = conn.cursor()
    #     results = curs.execute("SELECT month FROM consumptions WHERE company_id = ?",(self.id,))
    #     data = results.fetchall()
    #     conn.close()
    #     return data

    def __str__(self):
        '''         for e in self.elec:
            print(e)
        for e in self.water:
            print(e)
        for e in self.co2:
            print(e)
        for e in self.year:
            print(e)
        for e in self.month:
            print(e) '''
        #print(self.years)
        print(self.data)
        return self.name
