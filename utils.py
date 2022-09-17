
def get_values(data, the_year, the_month, type="electricity"):
    prev_year = False
    curr_month = the_month
    prev_month = 0
    
    if curr_month - 1 == 0:
        prev_month = 12
        prev_year = True
    else:
        prev_month = curr_month -1
    prev_value = 0
    cur_value = 0
    for year_data in data:
        for year in year_data:
            if year == the_year:
                if not prev_year:
                    for month_data in year_data[year]:
                        if month_data['month'] == prev_month:
                            prev_value = month_data[type]
                for month_data in year_data[year]:
                    if month_data['month'] == curr_month:
                        cur_value = month_data[type]

    if prev_year:
        for year_data in data:
            for year in year_data:
                if year == str(int(the_year) - 1):
                    for month_data in year_data[year]:
                        if month_data['month'] == "12":
                            prev_value = month_data[type]


    return prev_month, prev_value, curr_month, cur_value

# just one company. 
# def calculate_init_score(companies, year, month):
#     pharma_scores = []
#     software_scores = []
#     electrical_scores = []
#     retail_scores = []

#     for company in companies:
#         prev_month, prev_elec, curr_month, elec = get_values(company.data, year, month)
#         prev_month, prev_value, curr_month, water = get_values(company.data, year, month, type = "water")
#         prev_month, prev_value, curr_month, co2 = get_values(company.data, year, month, type = "co2")

#         score = (0.75*elec + 0.125*co2 + 0.125*water)

#         if company.industry =='Software & Tech Services':
#             software_scores.append({company.name: score})
#         elif company.industry =='Pharmaceutical':
#             pharma_scores.append({company.name: score})
#         elif company.industry =='Retail':
#             retail_scores.append({company.name: score})
#         elif company.industry =='Electrical Equipment & Parts':
#             electrical_scores.append({company.name: score})

#     return pharma_scores, software_scores, electrical_scores, retail_scores


