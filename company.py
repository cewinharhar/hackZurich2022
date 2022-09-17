# class with all the fields of the company
# in the main class for each field i need to call a mthod for that 
# specific field and sumarize into a dictionary

# imports
from db import get_db_connection, dict_factory

class Company:
    def __init__(self, name, company_id, industry, summary):

        # initalize the class with:
        self.name = name
        self.industry = industry
        self.id = company_id
        self.summary = summary

        # fetch from database:

        self.elec = self._get_electricity()
        
        self.water = self._get_water()

        self.co2 = self._get_co2()
        
        self.year =self._get_year()

        self.month = self._get_month()
        


    def _get_electricity(self):
        conn = get_db_connection()
        curs = conn.cursor()
        results = curs.execute("SELECT electricity FROM consumptions WHERE company_id = ?",(self.id,))
        data = results.fetchall()
        conn.close()
        return data

    def _get_water(self):
        conn = get_db_connection()
        curs = conn.cursor()
        results = curs.execute("SELECT water FROM consumptions WHERE company_id = ?",(self.id,))
        data = results.fetchall()
        conn.close()
        return data

    def _get_co2(self):
        conn = get_db_connection()
        curs = conn.cursor()
        results = curs.execute("SELECT co2 FROM consumptions WHERE company_id = ?",(self.id,))
        data = results.fetchall()
        conn.close()
        return data

    def _get_year(self):
        conn = get_db_connection()
        curs = conn.cursor()
        results = curs.execute("SELECT year FROM consumptions WHERE company_id = ?",(self.id,))
        data = results.fetchall()
        conn.close()
        return data

    def _get_month(self):
        conn = get_db_connection()
        curs = conn.cursor()
        results = curs.execute("SELECT month FROM consumptions WHERE company_id = ?",(self.id,))
        data = results.fetchall()
        conn.close()
        return data

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
        return self.name