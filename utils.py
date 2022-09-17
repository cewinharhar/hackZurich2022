
def get_values(data, the_year, the_month):
    prev_year = False
    curr_month = the_month
    prev_month = 0
    if curr_month - 1 == 0:
        prev_month = 12
        prev_year = True
    else:
        prev_month = curr_month -1
    prev_electricity = 0
    cur_electricity = 0
    for year_data in data:
        for year in year_data:
            if year == the_year:
                if not prev_year:
                    for month_data in year_data[year]:
                        if month_data['month'] == prev_month:
                            prev_electricity = month_data['electricity']
                for month_data in year_data[year]:
                    if month_data['month'] == curr_month:
                        cur_electricity = month_data['electricity']
                    
                        

    if prev_year:
        for year_data in data:
            for year in year_data:
                if year == str(int(the_year) - 1):
                    for month_data in year_data[year]:
                        if month_data['month'] == "12":
                            prev_electricity = month_data['electricity']

    



    return prev_month, prev_electricity, curr_month, cur_electricity