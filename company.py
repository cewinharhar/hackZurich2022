# class with all the fields of the company
# in the main class for each field i need to call a mthod for that 
# specific field and sumarize into a dictionary

# imports
import sqlite3

class Company:
    def __init__(self, name, electricity_usage, industry, 
                year, water_consumption, co2_emitted, summary):
        self.conn = sqlite3.connect("schema.sql")
        self.name = name
        self.elec = electricity_usage
        
        self.water = water_consumption
        self.co2 = co2_emitted
        self.industry = industry
        self.year = year
        self.summary = summary

    # method for calculating the % energy reduced / increased
    def calc_difference(self, type, previous_val):
        if type == "electricity":
            return (((self.elec - previous_val)/previous_val)*100)
        if type == "water":
            return (((self.water - previous_val)/previous_val)*100)
        if type == "co2":
            return (((self.co2 - previous_val)/previous_val)*100)

    # method for adding the current electricity to the current year
    def _add_usage(self):
        return { self.year:{"elec": self.elec, "water": self.water, "co2": self.co2}}
    

comp = Company("sbb", 1000, "train", 2022, 2000, 53, "man we like trains, foo, bar, bazzz")




