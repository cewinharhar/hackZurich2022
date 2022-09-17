import sqlite3
from werkzeug.exceptions import abort

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