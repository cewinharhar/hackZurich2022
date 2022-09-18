import sqlite3
from werkzeug.exceptions import abort
import statistics

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db_connection():
    conn = sqlite3.connect('database.db')
    #conn.row_factory = sqlite3.Row
    conn.row_factory = dict_factory
    return conn

def get_company(id):
    conn = get_db_connection()
    company = conn.execute('SELECT * FROM company WHERE id = ?',
                        (id,)).fetchone()
    conn.close()
    if company is None:
        abort(404)
    return company

def get_consumptions(company_id):
    conn = get_db_connection()
    consumptions = conn.execute('SELECT * FROM consumptions WHERE company_id = ?',
                        (company_id,)).fetchall()
    conn.close()
    if consumptions is None:
        abort(404)
    return consumptions

def get_last_date():
    conn = get_db_connection()
    last_year = conn.execute('SELECT DISTINCT year FROM consumptions ORDER BY year DESC').fetchone()
    last_month = conn.execute('SELECT DISTINCT month FROM consumptions where year = ? ORDER BY month DESC', (last_year['year'],)).fetchone()
    return last_month['month'], last_year['year']

def get_sd(type):
    conn = get_db_connection()
    if type == 'electricity':
        results = conn.execute("SELECT electricity FROM consumptions").fetchall()
    if type == 'water':
        results = conn.execute("SELECT water FROM consumptions").fetchall()
    conn.close()
    result = []
    for res in results:
        result.append(res[type])
    return statistics.stdev(result)

def get_total_mean_by_type(type):
    conn = get_db_connection()
    if type == 'electricity':
        results = conn.execute("SELECT SUM(electricity)/COUNT(electricity) AS mean FROM consumptions").fetchall()
    if type == 'water':
        results = conn.execute("SELECT SUM(water)/COUNT(water) AS mean FROM consumptions").fetchall()
    conn.close()
    result = 0
    for res in results:
        result = res['mean']
    return result

def get_values_by_year_and_type_and_comp(year, type, company_id):
    conn = get_db_connection()
    if type == 'electricity':
        results = conn.execute("SELECT electricity FROM consumptions WHERE year = ? and company_id = ?", ( year, company_id,)).fetchall()
    if type == 'water':
        results = conn.execute("SELECT water FROM consumptions WHERE year = ? and company_id = ?", ( year, company_id,)).fetchall()
    conn.close()
    result = []
    for res in results:
        result.append(res[type])
    return result