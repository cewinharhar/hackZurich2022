class Company:
    def __init__(self, name, electricity_usage_current, electricity_usage_previous, industry, year):
        self.name = name
        self.elec_current = electricity_usage_current
        self.elec_prev = electricity_usage_previous
        self.electricy_usage_per_year = {}
        self.industry = industry
        self.year = year


    def elec_difference(self):
        return (((self.elec_current - self.elec_prev)/self.elec_prev)*100)

    def add_electricity_usage(self):
        self.electricy_usage_per_year[self.year] = self.elec_current



comp = Company("sbb", 1000, 900, "manufactoring", 2022)
comp.add_electricity_usage()
print(comp.elec_difference(), comp.electricy_usage_per_year)
