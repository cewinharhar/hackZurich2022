# class with all the fields of the company
# in the main class for each field i need to call a mthod for that 
# specific field and sumarize into a dictionary

# imports
import sqlite3

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
        conn = sqlite3.connect("database.db")
        curs = conn.cursor()
        results = curs.execute("SELECT electricity FROM consumptions WHERE company_id == self.id")
        data = results.fetchall()
        conn.close()
        return data

    def _get_water(self):
        conn = sqlite3.connect("database.db")
        curs = conn.cursor()
        results = curs.execute("SELECT water FROM consumptions WHERE company_id == self.id")
        data = results.fetchall()
        conn.close()
        return data

    def _get_co2(self):
        conn = sqlite3.connect("database.db")
        curs = conn.cursor()
        results = curs.execute("SELECT co2 FROM consumptions WHERE company_id == self.id")
        data = results.fetchall()
        conn.close()
        return data

    def _get_year(self):
        conn = sqlite3.connect("database.db")
        curs = conn.cursor()
        results = curs.execute("SELECT year FROM consumptions WHERE company_id == self.id")
        data = results.fetchall()
        conn.close()
        return data

    def _get_month(self):
        conn = sqlite3.connect("database.db")
        curs = conn.cursor()
        results = curs.execute("SELECT month FROM consumptions WHERE company_id == self.id")
        data = results.fetchall()
        conn.close()
        return data


c = Company("sbb", 1, "health", "foo bar baz")

print(c.elec)