# class with all the fields of the company
# add a short summary of the company
class Company:
    def __init__(self, name, electricity_usage_current, electricity_usage_previous, industry, year):
        self.name = name
        self.elec_current = electricity_usage_current
        
        self.electricy_usage_per_year = {}
        self.industry = industry
        self.year = year

    # method for calculating the % energy reduced / increased
    def elec_difference(self, previous_elec):
        return (((self.elec_current - previous_elec)/previous_elec)*100)

    # method for adding the current electricity to the current year
    def add_electricity_usage(self):
        self.electricy_usage_per_year[self.year] = self.elec_current



comp = Company("sbb", 1000, "manufactoring", 2022)
comp.add_electricity_usage()
print(comp.elec_difference(900), comp.electricy_usage_per_year)
